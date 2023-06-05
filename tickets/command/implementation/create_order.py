from tickets.command.interface.command import *
from tickets.service.order import *

class CreateOrderCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        station_start_id = self.request.body['station_start_id']
        station_end_id = self.request.body['station_end_id']
        trip_id = self.request.body['trip_id']
        seats = self.request.body['seats']
        result = OrderService().create(station_start_id, station_end_id, trip_id, seats)
        return result