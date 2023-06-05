from django.db import models
from .carriage import *

class Seat(models.Model):
    id = models.IntegerField(primary_key=True)
    num = models.IntegerField()
    carriage = models.ForeignKey(Carriage, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return f"Seat(id={self.id}, num={self.num}, carriage_id={self.carriage})"
    
    class Meta:
        db_table = 'seat'