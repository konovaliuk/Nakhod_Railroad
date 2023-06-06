from django.db import models
from .train import *

class Trip(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return f"Trip(id={self.id}, train={self.train})"
    
    class Meta:
        db_table = 'trip'