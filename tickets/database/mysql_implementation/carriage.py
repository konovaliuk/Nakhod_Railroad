from tickets.database.interface.carriage import *
from tickets.database.entity.carriage import *
from tickets.database.entity.carriage_type import *
from tickets.database.entity.seat import *
from tickets.database.entity.trip import *
from tickets.database.entity.ticket import *
from tickets.database.entity.trip_station import *

class MysqlCarriage(ICarriage):
    def read_all(self):
        return Carriage.objects.all()

    def read(self, id):
        try:
            return Carriage.objects.get(id=id)
        except Carriage.DoesNotExist:
            return None
    
    def find(self, trip_id):
        subquery_carriage = Carriage.objects.filter(train_id=Trip.objects.filter(id=trip_id).values("train_id"))

        subquery_trip_station = TripStation.objects.filter(trip_id=trip_id).values("id")

        stmt = CarriageType.objects.filter(
            carriage__in=subquery_carriage,
            seat__id__notin=Ticket.objects.filter(trip_station_start_id__in=subquery_trip_station).values("seat_id")
        ).values("id", "name", "price_mod").annotate(count=models.Count())

        return stmt
    
