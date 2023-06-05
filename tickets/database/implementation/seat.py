from django.db import connection
from tickets.database.interface.seat import *
from tickets.database.entity.seat import *
from tickets.database.entity.carriage import *
from tickets.database.entity.trip import *
from tickets.database.entity.trip_station import *
from tickets.database.entity.ticket import *

class SeatImpl(ISeat):
    def read_all(self):
        return Seat.objects.all()

    def read(self, id):
        try:
            return Seat.objects.get(id=id)
        except Seat.DoesNotExist:
            return None
    
    def find(self, trip, train, ctype, from_station, to_station):
        result = None
        query = f"SELECT carriage_id, GROUP_CONCAT(id), GROUP_CONCAT(num) FROM seat WHERE carriage_id IN(SELECT id FROM carriage WHERE carriage_type_id={ctype} AND train_id=(SELECT train_id FROM trip WHERE id={trip})) AND seat.id NOT IN (SELECT seat_id FROM ticket WHERE trip_station_start_id IN (SELECT id FROM trip_station WHERE trip_id = {trip})) GROUP BY carriage_id;"
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()

        result = []
        for carriage in data:
            obj = {'id': carriage[0], 'seats': []}
            for seat in zip(carriage[1].split(','), carriage[2].split(',')):
                obj['seats'].append({
                    'id': int(seat[0]),
                    'num': int(seat[1])
                })
            result.append(obj)
        return result
