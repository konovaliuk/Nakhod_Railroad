from tickets.command.interface.command import *
from tickets.service.profile import *

class ReadProfileCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        result = ProfileService().read(self.request)
        return result