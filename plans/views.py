from rest_framework import viewsets
from .models import ServicePlan
from .serializers import ServicePlanSerializer
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsGuest
class ServicePlanViewSet(viewsets.ModelViewSet):
    permission_classes=[IsGuest]
    queryset = ServicePlan.objects.all()
    serializer_class = ServicePlanSerializer
