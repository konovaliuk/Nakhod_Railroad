from tickets.command.interface.command import *
from tickets.service.auth import *

class ResetPasswordCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        password = self.request.body['password']
        result = AuthService().reset_password(password)
        return result