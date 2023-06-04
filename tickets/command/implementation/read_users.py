from tickets.command.interface.command import *
from tickets.service.admin import *

class ReadUsersCommand(ICommand):
    def __init__(self):
        pass
        
    def execute(self):
        result = AdminService().read_users()
        return result