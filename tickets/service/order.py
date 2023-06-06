import json
import os
from dotenv import load_dotenv
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from tickets.database.entity.ticket import *
from tickets.database.entity.trip_station import *
from tickets.database.entity.station import *
from tickets.database.implementation.station import *
from tickets.database.implementation.trip import *
from tickets.database.implementation.train import *
from tickets.database.implementation.trip_station import *
from tickets.database.implementation.seat import *
from tickets.database.implementation.carriage import *
from tickets.database.implementation.carriage_type import *
from tickets.database.implementation.ticket import *
import stripe
import random
import string
import os
import qrcode
from dotenv import load_dotenv
import pdfkit
from tickets.service.mail import *
import base64

class OrderService:
    def read(self, request):
        if not request.session.get('logged_in'):
            return redirect(reverse('index'))
        ticket_table = TicketImpl()
        trip_station_table = TripStationImpl()
        station_table = StationImpl()
        
        tickets = ticket_table.find(request.session['id'])
        data = {'tickets': [], 'session': dict(request.session)}
        for ticket in tickets:
            ticket_info = ticket_table.info(ticket.id)
            trip_station_start = trip_station_table.read(ticket_info['trip_station_start_id'])
            trip_station_end = trip_station_table.read(ticket_info['trip_station_end_id'])
            station_start = station_table.read(trip_station_start.station_id)
            station_end = station_table.read(trip_station_end.station_id)
            data['tickets'].append({
                'id': ticket_info['id'],
                'station_start_name': station_start.name,
                'station_end_name': station_end.name,
                'time_dep': trip_station_start.time_dep
            })
        return render(request, 'orders.html', context=data)
    
    def create(self, request):
        if not request.session.get('logged_in'):
            return JsonResponse({'msg': 'Please login to create an order'}, status=401)
        station_start_id = json.loads(request.body)['station_start_id']
        station_end_id = json.loads(request.body)['station_end_id']
        trip_id = json.loads(request.body)['trip_id']
        seats = json.loads(request.body)['seats']
        load_dotenv()
        public_url = f"{os.getenv('DOMAIN')}"
        stripe.api_key = os.getenv('STRIPE_API_KEY')
        user_id = request.session['id']
        public_url = f"{os.getenv('DOMAIN')}"
        station_table = StationImpl()
        trip_table = TripImpl()
        user_id = request.session['id']
        train_table = TrainImpl()
        trip_station_table = TripStationImpl()
        carriage_table = CarriageImpl()
        carriage_type_table = CarriageTypeImpl()
        seat_table = SeatImpl()
        
        station_start = station_table.read(station_start_id)
        station_end = station_table.read(station_end_id)
        trip_station_start = trip_station_table.find(trip_id, station_start_id)
        trip_station_end = trip_station_table.find(trip_id, station_end_id)
        trip = trip_table.read(trip_id)
        train = train_table.read(trip.train_id)
        line_items = []
        for seat_id in seats:
            seat = seat_table.read(seat_id)
            carriage = carriage_table.read(seat.carriage_id)
            carriage_type = carriage_type_table.read(carriage.carriage_type_id)
            train = train_table.read(carriage.train_id)
            name = f"{station_start.name} - {station_end.name}, Train {train.name}, Carriage {carriage.num}, Seat: {seat.num}"
            line_items.append({
                'price_data': {
                    'currency': 'uah',
                    'unit_amount': (trip_station_end.price - trip_station_start.price) * carriage_type.price_mod,
                    'product_data': {
                        'name': name,
                        'metadata': {
                            'user_id': user_id,
                            'seat_id': seat.id,
                            'trip_station_start_id': trip_station_start.id,
                            'trip_station_end_id': trip_station_end.id
                        }
                    },
                },
                'quantity': 1
            })
        checkout_session = stripe.checkout.Session.create(
            success_url=f"{public_url}{reverse('orders')}",
            cancel_url=f"{public_url}{reverse('seats')}?trip={trip.id}&ctype={carriage_type.id}&from={station_start.id}&to={station_end.id}",
            line_items=line_items,
            mode='payment'
        )
        return JsonResponse({'url': f'{checkout_session.url}'}, status=200)
    
    def complete(self, request):
        payload = request.body.decode('utf-8')
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        checkout_session_id = json.loads(request.body)['data']['object']['id']
        stripe.api_key = os.getenv('STRIPE_API_KEY')
        endpoint_secret = os.getenv('STRIPE_ENDPOINT_KEY')
        event = None
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            return JsonResponse({'msg': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return JsonResponse({'msg': 'This request didn\'t come from Stripe'}, status=400)

        checkout_session = stripe.checkout.Session.retrieve(
            checkout_session_id,
            expand=['line_items']
        )
        
        ticket_ids = []
        attachments = []
        user_email = None
        user_id = None
        for item in checkout_session['line_items']['data']:
            product = stripe.Product.retrieve(
                item['price']['product']
            )
            metadata = product['metadata']
            ticket_table = TicketImpl()
            ticket_id = ticket_table.create(Ticket(
                user_id=metadata['user_id'],
                seat_id=metadata['seat_id'],
                trip_station_start_id=metadata['trip_station_start_id'],
                trip_station_end_id=metadata['trip_station_end_id'],
                token=''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            ))
            ticket_ids.append(ticket_id)
        user_table = UserImpl()
        ticket_table = TicketImpl()
        trip_station_table = TripStationImpl()
        station_table = StationImpl()
        for id in ticket_ids:
            ticket_info = ticket_table.info(id)
            trip_station_start = trip_station_table.read(ticket_info['trip_station_start_id'])
            trip_station_end = trip_station_table.read(ticket_info['trip_station_end_id'])
            station_start = station_table.read(trip_station_start.station_id)
            station_end = station_table.read(trip_station_end.station_id)
            ticket_id = ticket_info['id']
            qrcode = self.create_qrcode(request, ticket_id, bypass_verification=True)
            data = {'status': 'valid',
                'ticket': {
                    'id': ticket_id,
                    'train_name': ticket_info['seat__carriage__train__name'],
                    'carriage_num': ticket_info['seat__carriage__num'],
                    'seat_num': ticket_info['seat__num'],
                    'station_start_name': station_start.name,
                    'station_end_name': station_end.name,
                    'time_dep': trip_station_start.time_dep,
                    'time_arr': trip_station_end.time_arr,
                    'user_email': ticket_info['user__email'],
                    'qrcode': qrcode
                }, 'session': dict(request.session)}
            user_email = ticket_info['user__email']
            user_name = ticket_info['user__name']
            pdfkit.from_string(render_to_string('ticket.html', context=data), f'ticket-{ticket_id}.pdf', css='tickets/static/styles/ticket.css')
            with open(f'ticket-{ticket_id}.pdf', 'rb') as f:
                data = f.read()
                f.close()
                os.remove(f'ticket-{ticket_id}.pdf')
            
            encoded_file = base64.b64encode(data).decode()
            attachedFile = Attachment(
                FileContent(encoded_file),
                FileName(f'ticket-{ticket_id}.pdf'),
                FileType('application/pdf'),
                Disposition('attachment')
            )
            attachments.append(attachedFile)
        dynamic_template_data = {
            'name': user_name,
            'order_url': f'{os.getenv("DOMAIN")}{reverse("orders")}'
        }
        response = MailService().send(
            to_email=user_email,
            template_id='d-dfac0b55f330431bb84397dabfdf1e9e',
            dynamic_template_data=dynamic_template_data,
            attachments=attachments
        )
        return response
    
    def verify(self, id, token):
        engine = current_app.config['engine']
        ticket_table = current_app.config['tables']['ticket']
        trip_station_table = current_app.config['tables']['trip_station']
        station_table = current_app.config['tables']['station']
        with Session(engine) as s:
            ticket = ticket_table.verify(s, id, token)
            if not ticket:
                data = {'status': 'invalid'}
            else:
                ticket_info = ticket_table.info(s, id)
                trip_station_start = trip_station_table.read(s, ticket_info[4])
                trip_station_end = trip_station_table.read(s, ticket_info[5])
                station_start = station_table.read(s, trip_station_start.station_id)
                station_end = station_table.read(s, trip_station_end.station_id)
                data = {'status': 'valid',
                    'ticket': {
                        'id': ticket_info[0],
                        'train_name': ticket_info[1],
                        'carriage_num': ticket_info[2],
                        'seat_num': ticket_info[3],
                        'station_start_name': station_start.name,
                        'station_end_name': station_end.name,
                        'time_dep': trip_station_start.time_dep,
                        'time_arr': trip_station_end.time_arr,
                        'user_email': ticket_info[6]
                    }, 'session': dict(request.session)}
        return render_template('verify.html', data=data)
    
    def create_qrcode(self, request, ticket_id, bypass_verification=False):
        if not bypass_verification and (not request.session.get('logged_in')):
            return redirect(reverse('index'))
        ticket_table = TicketImpl()
        
        ticket = ticket_table.read(ticket_id)
        public_url = f"{os.getenv('DOMAIN')}"
        if not bypass_verification and ticket.user_id != request.session.get('id'):
            return redirect(url_for('index'))
        img = qrcode.make(f"{public_url}{reverse('verify')}?id={ticket_id}&token={ticket.token}")
        img_path = f'qrcode-{ticket_id}.png'
        img.save(img_path)
        if bypass_verification:
            with open(img_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                response = encoded_string
        else:
            with open(img_path, "rb") as image_file:
                response = HttpResponse(image_file, content_type='image/png')
        return response