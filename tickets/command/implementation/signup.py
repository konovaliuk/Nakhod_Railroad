from tickets.command.interface.command import *
from tickets.service.auth import *

class SignupCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        name = self.request.body['name']
        email = self.request.body['email']
        password = self.request.body['password']
        result = AuthService().signup(name, email, password)
        return result