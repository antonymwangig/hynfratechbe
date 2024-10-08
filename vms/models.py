import uuid
from django.db import models

from users.models import User

class VirtualMachine(models.Model):
    VM_STATES = [
        ('Running', 'Running'),
        ('Blocked', 'Blocked'),
        ('Paused', 'Paused'),
        ('Shutdown', 'Shutdown'),        
        ('Shutoff', 'Shutoff'),        
        ('Crashed', 'Crashed'),        
        ('No state', 'No state'),
        ('Unknown', 'Unknown'),
    ]
    name = models.CharField(max_length=100)
    vm_name= models.CharField(max_length=100,unique=True)
    state = models.CharField(max_length=10, choices=VM_STATES, default='Unknown')
    vcpu_count = models.IntegerField(default=1)
    memory_size = models.IntegerField(help_text='Memory size in KIB')
    disk_size = models.IntegerField(help_text='Disk size in GB')
    disk_image_path=models.CharField(max_length=1000, unique=True)    
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        permissions = [
            ("can_change_vm_owner", "Move VMs between users"),
        ]
