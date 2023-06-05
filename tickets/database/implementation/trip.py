from django.db import connection
from tickets.database.interface.trip import *
from tickets.database.entity.trip import *
from tickets.database.entity.trip_station import *

class TripImpl(ITrip):
    def read_all(self):
        return Trip.objects.all()

    def read(self, id):
        try:
            return Trip.objects.get(id=id)
        except Trip.DoesNotExist:
            return None
    
    def find(self, station_start, station_end, depart_date):
        result = None
        query = f'SELECT t1.trip_id, t1.time_dep, t2.time_arr, t2.price-t1.price FROM trip_station t1, trip_station t2 WHERE t1.station_id = {station_start} AND t2.station_id = {station_end} AND t1.trip_id = t2.trip_id AND t1.num < t2.num AND DATE(t1.time_dep) = "{depart_date}" GROUP BY t1.trip_id, t1.time_dep, t2.time_arr, t1.price, t2.price;'
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        
        return result

    
