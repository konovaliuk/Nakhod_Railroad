from django.db import models
from .user import *
from .seat import *
from .trip_station import *

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    trip_station_start = models.ForeignKey(TripStation, on_delete=models.CASCADE, related_name='trip_station_start')
    trip_station_end = models.ForeignKey(TripStation, on_delete=models.CASCADE, related_name='trip_station_end')
    token = models.CharField(max_length=60)

    def __repr__(self) -> str:
        return f"Ticket(id={self.id}, user={self.user}, seat={self.seat}, trip_station_start={self.trip_station_start}, trip_station_end={self.trip_station_end}, token={self.token})"
    
    class Meta:
        db_table = 'ticket'
