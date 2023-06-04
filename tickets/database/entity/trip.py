from django.db import models
from .train import *

class Trip(models.Model):
    id = models.IntegerField(primary_key=True)
    train_id = models.ForeignKey(Train, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return f"Trip(id={self.id}, train_id={self.train_id})"