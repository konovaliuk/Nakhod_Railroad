from tickets.database.interface.ticket import *
from tickets.database.entity.ticket import *
from tickets.database.entity.train import *
from tickets.database.entity.carriage import *
from tickets.database.entity.seat import *
from tickets.database.entity.user import *

class TicketImpl(ITicket):
    def read_all(self):
        return Ticket.objects.all()

    def read(self, id):
        try:
            return Ticket.objects.get(id=id)
        except Ticket.DoesNotExist:
            return None

    def create(self, ticket):
        new_ticket = Ticket(
            user_id=ticket.user_id,
            seat_id=ticket.seat_id,
            trip_station_start_id=ticket.trip_station_start_id,
            trip_station_end_id=ticket.trip_station_end_id,
            token=ticket.token
        )
        new_ticket.save()
        return new_ticket.id

    def find(self, user_id):
        return Ticket.objects.filter(user_id=user_id)
    
    def info(self, id):
        return Ticket.objects.filter(id=id).values(
            'id',
            'seat__carriage__train__name',
            'seat__carriage__num',
            'seat__num',
            'trip_station_start_id',
            'trip_station_end_id',
            'user__email',
            'user__name'
        ).first()
    
    def verify(self, id, token):
        try:
            return Ticket.objects.get(id=id, token=token)
        except Ticket.DoesNotExist:
            return None