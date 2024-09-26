from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VirtualMachineViewSet, CreateVMAPIView,StartVMAPIView,VMStateView

router = DefaultRouter()
router.register(r'virtual-machines', VirtualMachineViewSet, basename='virtualmachine')

urlpatterns = [
    path('', include(router.urls)),
    path('create-virtual-machine/', CreateVMAPIView.as_view(), name='create-virtual-machine'),
    path('start-virtual-machine/', StartVMAPIView.as_view(), name='start-virtual-machine'),
    path('vm-state/', VMStateView.as_view(), name='vm-state'),

]
