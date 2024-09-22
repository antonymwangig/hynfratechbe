import uuid
from django.db import models

class ServicePlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()  
    def __str__(self):
        return self.name
