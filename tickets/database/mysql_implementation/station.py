from tickets.database.interface.station import *
from tickets.database.entity.station import *

class MysqlStation(IStation):
    def read_all(self):
        return Station.objects.all()

    def read(self, id):
        try:
            return Station.objects.get(id=id)
        except Station.DoesNotExist:
            return None

    def find(self, query):
        return Station.objects.filter(name__startswith=query)

