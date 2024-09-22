from rest_framework import viewsets
from .models import ServicePlan
from .serializers import ServicePlanSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ServicePlanFilter

class ServicePlanViewSet(viewsets.ModelViewSet):
    queryset = ServicePlan.objects.all()
    serializer_class = ServicePlanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServicePlanFilter  # Use the custom filterset
