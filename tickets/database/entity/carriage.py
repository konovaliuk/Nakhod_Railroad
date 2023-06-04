from django.db import models
from .train import *
from .carriage_type import *

class Carriage(models.Model):
    id = models.IntegerField(primary_key=True)
    num = models.IntegerField()
    train_id = models.ForeignKey(Train, on_delete=models.CASCADE)
    carriage_type_id = models.ForeignKey(CarriageType, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return f"Carriage(id={self.id}, num={self.num}, train_id={self.train_id}, carriage_type_id={self.carriage_type_id})"