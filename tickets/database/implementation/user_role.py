from tickets.database.interface.user_role import *
from tickets.database.entity.user_role import *

class UserRoleImpl(IUserRole):
    def read_all(self):
        return UserRole.objects.all()

    def read(self, id):
        try:
            return UserRole.objects.get(id=id)
        except UserRole.DoesNotExist:
            return None
