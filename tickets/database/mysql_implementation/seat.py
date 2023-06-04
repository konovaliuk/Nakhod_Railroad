from tickets.database.interface.seat import *
from tickets.database.entity.seat import *
from tickets.database.entity.carriage import *
from tickets.database.entity.trip import *
from tickets.database.entity.trip_station import *
from tickets.database.entity.ticket import *

class MysqlSeat(ISeat):
    def read_all(self):
        return Seat.objects.all()

    def read(self, id):
        try:
            return Seat.objects.get(id=id)
        except Seat.DoesNotExist:
            return None
    
    def find(self, trip, train, ctype, from_station, to_station):
        subquery_carriage = Carriage.objects.filter(carriage_type_id=ctype, train_id=Trip.objects.filter(id=trip).values("train_id"))

        subquery_trip_station = TripStation.objects.filter(trip_id=1).values("id")

        stmt = Seat.objects.filter(
            carriage_id__in=subquery_carriage,
            id__notin=Ticket.objects.filter(trip_station_start_id__in=subquery_trip_station).values("seat_id")
        ).values("carriage_id").annotate(
            seats=models.Func(models.F("id"), function="GROUP_CONCAT"),
            nums=models.Func(models.F("num"), function="GROUP_CONCAT")
        )

        result = []
        for carriage in stmt:
            obj = {'id': carriage['carriage_id'], 'seats': []}
            seats = carriage['seats'].split(',')
            nums = carriage['nums'].split(',')
            for seat, num in zip(seats, nums):
                obj['seats'].append({
                    'id': int(seat),
                    'num': int(num)
                })
            result.append(obj)
        return result
