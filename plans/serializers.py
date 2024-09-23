from rest_framework import serializers
from .models import ServicePlan

class ServicePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePlan
        fields = ['id', 'name', 'price', 'features']
        read_only_fields = ['id']
