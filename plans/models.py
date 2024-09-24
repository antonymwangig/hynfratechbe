import uuid
from django.db import models

class ServicePlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField() 
    vcpu_count = models.IntegerField(default=1)
    memory_size = models.IntegerField(help_text='Memory size in KIB')
    disk_size = models.IntegerField(help_text='Disk size in GB')
 
    def __str__(self):
        return self.name
