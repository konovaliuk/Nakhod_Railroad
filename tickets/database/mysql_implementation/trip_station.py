from tickets.database.interface.trip_station import *
from tickets.database.entity.trip_station import *

class MysqlTripStation(ITripStation):
    def read_all(self):
        return TripStation.objects.all()

    def read(self, id):
        try:
            return TripStation.objects.get(id=id)
        except TripStation.DoesNotExist:
            return None
    
    def info(self, trip_id, station_start, station_end):
        t1 = TripStation.objects.filter(trip_id=trip_id, station_id=station_start).first()
        t2 = TripStation.objects.filter(trip_id=trip_id, station_id=station_end).first()
        if t1 and t2:
            return t1.time_dep, t2.time_arr, t2.price - t1.price
        return None
    
    def find(self, trip_id, station_id):
        try:
            return TripStation.objects.get(trip_id=trip_id, station_id=station_id)
        except TripStation.DoesNotExist:
            return None
    

    
