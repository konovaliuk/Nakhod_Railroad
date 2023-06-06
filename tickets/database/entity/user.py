from django.db import models
from .user_role import *

class User(models.Model):
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password_hash = models.CharField(max_length=60)
    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    confirmed_email = models.BooleanField()
    confirm_email_token = models.CharField(max_length=60)
    reset_password_token = models.CharField(max_length=60)

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name})"
    
    class Meta:
        db_table = 'user'