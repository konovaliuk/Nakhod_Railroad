from django.db import connection
from tickets.database.interface.carriage import *
from tickets.database.entity.carriage import *
from tickets.database.entity.carriage_type import *
from tickets.database.entity.seat import *
from tickets.database.entity.trip import *
from tickets.database.entity.ticket import *
from tickets.database.entity.trip_station import *

class CarriageImpl(ICarriage):
    def read_all(self):
        return Carriage.objects.all()

    def read(self, id):
        try:
            return Carriage.objects.get(id=id)
        except Carriage.DoesNotExist:
            return None
    
    def find(self, trip_id):
        result = None
        query = f"SELECT carriage_type.id, carriage_type.name, carriage_type.price_mod, count(*) FROM seat JOIN carriage ON seat.carriage_id = carriage.id JOIN carriage_type ON carriage.carriage_type_id = carriage_type.id WHERE carriage_id in (SELECT id FROM carriage WHERE train_id = (SELECT train_id FROM trip WHERE id = {trip_id})) AND seat.id NOT IN (SELECT seat_id FROM ticket WHERE trip_station_start_id IN (SELECT id FROM trip_station WHERE trip_id = 1)) GROUP BY carriage_type.id, carriage_type.name;"
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        
        return result
    
