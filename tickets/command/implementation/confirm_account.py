from tickets.command.interface.command import *
from tickets.service.auth import *

class ConfirmAccountCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        id = self.request.GET.get('id')
        token = self.request.GET.get('token')
        result = AuthService().confirm(id, token)
        return result