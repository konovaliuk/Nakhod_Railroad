from tickets.command.interface.command import *
from tickets.service.auth import *

class LogoutCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        result = AuthService().logout(self.request)
        return result