from django.db import models
from .train import *
from .carriage_type import *

class Carriage(models.Model):
    id = models.IntegerField(primary_key=True)
    num = models.IntegerField()
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    carriage_type = models.ForeignKey(CarriageType, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return f"Carriage(id={self.id}, num={self.num}, train={self.train}, carriage_type={self.carriage_type})"
    
    class Meta:
        db_table = 'carriage'