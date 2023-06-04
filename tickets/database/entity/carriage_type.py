from django.db import models

class CarriageType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    price_mod = models.IntegerField()

    def __repr__(self) -> str:
        return f"CarriageType(id={self.id}, name={self.name}, price_mod={self.price_mod})"