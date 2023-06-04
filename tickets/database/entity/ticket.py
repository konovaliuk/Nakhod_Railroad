from django.db import models
from .user import *
from .seat import *
from .trip_station import *

class Ticket(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    seat_id = models.ForeignKey(Seat, on_delete=models.CASCADE)
    trip_station_start_id = models.ForeignKey(TripStation, on_delete=models.CASCADE, related_name='trip_station_start_id')
    trip_station_end_id = models.ForeignKey(TripStation, on_delete=models.CASCADE, related_name='trip_station_end_id')
    token = models.CharField(max_length=60)

    def __repr__(self) -> str:
        return f"Ticket(id={self.id}, user_id={self.user_id}, seat_id={self.seat_id}, trip_station_start_id={self.trip_station_start_id}, trip_station_end_id={self.trip_station_end_id}, token={self.token})"
