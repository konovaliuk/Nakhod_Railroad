from django.db import models
from .trip import *
from .station import *

class TripStation(models.Model):
    id = models.IntegerField(primary_key=True)
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    station_id = models.ForeignKey(Station, on_delete=models.CASCADE)
    num = models.IntegerField()
    time_arr = models.DateField()
    time_dep = models.DateField()
    price = models.IntegerField()

    def __repr__(self) -> str:
        return f"TripStation(id={self.id}, trip_id={self.trip_id}, station_id={self.station_id}, num={self.num}, time_arr={self.time_arr}, time_dep={self.time_dep}, price={self.price})"