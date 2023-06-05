from tickets.command.interface.command import *
from tickets.service.order import *

class VerifyOrderCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        id = self.request.GET.get('id')
        token = self.request.GET.get('token')
        result = OrderService().verify(id, token)
        return result