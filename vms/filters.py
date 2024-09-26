import django_filters
from .models import VirtualMachine

class VirtualMachineFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    state = django_filters.ChoiceFilter(choices=VirtualMachine.VM_STATES) 
    class Meta:
        model = VirtualMachine
        fields = ['name', 'state']