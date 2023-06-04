from tickets.command.interface.command import *
from tickets.service.auth import *

class LogoutCommand(ICommand):
    def __init__(self):
        pass
        
    def execute(self):
        result = AuthService().logout()
        return result