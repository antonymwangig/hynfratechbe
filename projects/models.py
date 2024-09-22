import uuid
from django.db import models
from users.models import User  

class Project(models.Model):
    name = models.CharField(max_length=255)  
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
