from django.http import JsonResponse
from django.shortcuts import render
from tickets.database.entity.user import *
from tickets.database.implementation.station import *
from tickets.database.implementation.trip import *
from tickets.database.implementation.train import *
from tickets.database.implementation.trip_station import *
from tickets.database.implementation.carriage import *
from tickets.database.implementation.seat import *
from tickets.database.implementation.carriage_type import *
import datetime

class SearchService:
    def search_tickets(self, request):
        from_station = request.GET.get('from')
        to_station = request.GET.get('to')
        depart_date = request.GET.get('depart')
        trip_table = TripImpl()
        carriage_table = CarriageImpl()
        train_table = TrainImpl()
        station_table = StationImpl()
        trips = trip_table.find(from_station, to_station, depart_date)
        data = {'trips': [], 'session': dict(request.session)}
        for trip in trips:
            carriage_seats = carriage_table.find(trip[0])
            carriage_seats_formatted = []
            for carriage_seat in carriage_seats:
                carriage_seats_formatted.append(
                    {
                        'carriage_id': carriage_seat[0],
                        'carriage_type': carriage_seat[1],
                        'seat_price': int(trip[3] * carriage_seat[2]),
                        'seat_quantity': carriage_seat[3]
                    }
                )
            if not carriage_seats_formatted:
                continue
            train = train_table.read(trip[0])
            duration_seconds = (trip[2] - trip[1]).total_seconds()
            hours = int(duration_seconds//3600)
            minutes = int((duration_seconds - hours * 3600)//60)
            duration = f'{hours} h {minutes} min'
            data['trips'].append({
                'id': trip[0],
                'train_id': train.id,
                'train_name': train.name,
                'time_dep': trip[1],
                'time_arr': trip[2],
                'time_dep_pretty': trip[1].strftime('%H:%M'),
                'time_arr_pretty': trip[2].strftime('%H:%M'),
                'duration_pretty': duration,
                'base_price': trip[3],
                'carriage_seats': carriage_seats_formatted
            })
        station_start = station_table.read(from_station)
        station_end = station_table.read(to_station)
        data['station_start_name'] = station_start.name
        data['station_start_id'] = station_start.id
        data['station_end_name'] = station_end.name
        data['station_end_id'] = station_end.id
        data['depart_date'] = datetime.datetime.strptime(depart_date, '%Y-%m-%d').strftime('%a, %b %d %Y')
        return render(request, 'search.html', context=data)
    
    def search_seats(self, request):
        trip_id = request.GET.get('trip')
        ctype = request.GET.get('ctype')
        from_station = request.GET.get('from')
        to_station = request.GET.get('to')
        trip_table = TripImpl()
        train_table = TrainImpl()
        seat_table = SeatImpl()
        trip_station_table = TripStationImpl()
        station_table = StationImpl()
        carriage_type_table = CarriageTypeImpl()
        train = train_table.find(trip_id)
        carriages = seat_table.find(trip_id, train.id, ctype, from_station, to_station)
        station_start = station_table.read(from_station)
        station_end = station_table.read(to_station)
        trip_extra_info = trip_station_table.info(trip_id, from_station, to_station)
        carriage_type = carriage_type_table.read(ctype)
        data = {
            'carriages': carriages,
            'trip_id': trip_id,
            'train_id': train.id,
            'train_name': train.name,
            'station_start_name': station_start.name,
            'station_start_id': station_start.id,
            'station_end_name': station_end.name,
            'station_end_id': station_end.id,
            'carriage_type_id': ctype,
            'carriage_type_name': carriage_type.name,
            'price': int(trip_extra_info[2] * carriage_type.price_mod),
            'depart_date': trip_extra_info[0].strftime('%Y-%m-%d'),
            'depart_date_pretty': trip_extra_info[0].strftime('%a, %b %d %Y'),
            'time_dep_pretty': trip_extra_info[0].strftime('%H:%M'),
            'time_arr_pretty': trip_extra_info[1].strftime('%H:%M'),
            'session': dict(request.session)
        }
        return render(request, 'seats.html', context=data)
    
    def search_stations(self, request):
        query = request.GET.get('q')
        result = []
        stations = StationImpl().find(query)
        
        for station in stations:
            d = station.__dict__
            d.pop('_state', None)
            result.append(d)
        return JsonResponse(result, safe=False)