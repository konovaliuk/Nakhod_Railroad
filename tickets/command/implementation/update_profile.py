from tickets.command.interface.command import *
from tickets.service.profile import *

class UpdateProfileCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        fields = self.request.body['fields']
        password = None
        try:
            password = self.request.body['password']
        except:
            pass
        result = ProfileService().update(fields, password)
        return result