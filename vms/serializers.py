from rest_framework import serializers
from .models import VirtualMachine

class VirtualMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualMachine
        fields = ['id', 'name', 'state', 'vcpu_count', 'memory_size', 'disk_size', 'mac_address', 'ip_address',  'created_at']
        read_only_fields = ['id', 'created_at']
