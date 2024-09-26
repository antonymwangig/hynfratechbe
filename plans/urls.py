from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServicePlanViewSet

router = DefaultRouter()
router.register(r'service-plans', ServicePlanViewSet, basename='service-plans')

urlpatterns = [
    path('', include(router.urls)),
]
