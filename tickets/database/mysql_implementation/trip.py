from tickets.database.interface.trip import *
from tickets.database.entity.trip import *
from tickets.database.entity.trip_station import *

class MysqlTrip(ITrip):
    def read_all(self):
        return Trip.objects.all()

    def read(self, id):
        try:
            return Trip.objects.get(id=id)
        except Trip.DoesNotExist:
            return None
    
    def find(self, station_start, station_end, depart_date):
        t1 = TripStation.objects.filter(station_id=station_start)
        t2 = TripStation.objects.filter(station_id=station_end, trip_id=t1.values("trip_id"), num__gt=t1.values("num"), time_dep__date=depart_date)
        stmt = t1.annotate(time_arr=models.Subquery(t2.values("time_arr")[:1]), price_difference=models.ExpressionWrapper(t2.values("price")[:1] - t1.values("price")[:1], output_field=models.IntegerField())).values("trip_id", "time_dep", "time_arr", "price_difference")
        result = session.execute(stmt)
        return result

    
