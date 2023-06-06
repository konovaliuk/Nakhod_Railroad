from django.db import models

class UserRole(models.Model):
    name = models.CharField(max_length=60)

    def __repr__(self) -> str:
        return f"UserRole(id={self.id}, name={self.name})"
    
    class Meta:
        db_table = 'user_role'
