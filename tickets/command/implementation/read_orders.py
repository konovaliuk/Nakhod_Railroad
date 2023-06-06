from tickets.command.interface.command import *
from tickets.service.order import *

class ReadOrdersCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        result = OrderService().read(self.request)
        return result