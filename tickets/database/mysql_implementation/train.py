from tickets.database.interface.train import *
from tickets.database.entity.train import *
from tickets.database.entity.trip import *

class MysqlTrain(ITrain):
    def read_all(self):
        return Train.objects.all()

    def read(self, id):
        try:
            return Train.objects.get(id=id)
        except Train.DoesNotExist:
            return None

    def find(self, trip_id):
        subquery = Trip.objects.filter(id=trip_id).values("train_id")
        try:
            train_id = subquery[0]["train_id"]
            return Train.objects.get(id=train_id)
        except IndexError:
            return None
        except Train.DoesNotExist:
            return None

    
