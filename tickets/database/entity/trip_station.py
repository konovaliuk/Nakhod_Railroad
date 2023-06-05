from django.db import models
from .trip import *
from .station import *

class TripStation(models.Model):
    id = models.IntegerField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    num = models.IntegerField()
    time_arr = models.DateField()
    time_dep = models.DateField()
    price = models.IntegerField()

    def __repr__(self) -> str:
        return f"TripStation(id={self.id}, trip={self.trip}, station={self.station}, num={self.num}, time_arr={self.time_arr}, time_dep={self.time_dep}, price={self.price})"
    
    class Meta:
        db_table = 'trip_station'