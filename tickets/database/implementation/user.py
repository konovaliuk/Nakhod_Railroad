from tickets.database.interface.user import *
from tickets.database.entity.user import *
import bcrypt

class UserImpl(IUser):
    def read_all(self):
        return User.objects.all()

    def read(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def create(self, user, password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        new_user = User.objects.create_user(username=user.name, email=user.email, password_hash=password_hash, user_role_id=user.user_role_id, confirm_email_token=user.confirm_email_token)
        return new_user.id

    def update(self, id, fields):
        user = User.objects.get(id=id)
        for key, value in fields.items():
            if key == 'password':
                user.set_password(value)
            else:
                setattr(user, key, value)
        user.save()
            
    def find(self, email, password=None):
        try:
            user = User.objects.get(email=email)
            if (user == None or password == None or bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))):
                return user
        except User.DoesNotExist:
            pass
        return None
