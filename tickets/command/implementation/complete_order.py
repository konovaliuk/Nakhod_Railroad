from tickets.command.interface.command import *
from tickets.service.order import *

class CompleteOrderCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        payload = self.request.body
        sig_header = self.request.headers.get('Stripe-Signature')
        checkout_session_id = self.request.body['data']['object']['id']
        result = OrderService().complete(payload, sig_header, checkout_session_id)
        return result