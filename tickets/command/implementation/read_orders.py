from tickets.command.interface.command import *
from tickets.service.order import *

class ReadOrdersCommand(ICommand):
    def __init__(self):
        pass
        
    def execute(self):
        result = OrderService().read()
        return result