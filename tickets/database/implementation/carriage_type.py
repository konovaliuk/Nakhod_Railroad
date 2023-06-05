from tickets.database.interface.carriage_type import *
from tickets.database.entity.carriage_type import *

class CarriageTypeImpl(ICarriageType):
    def read_all(self):
        return CarriageType.objects.all()

    def read(self, id):
        try:
            return CarriageType.objects.get(id=id)
        except CarriageType.DoesNotExist:
            return None

    
