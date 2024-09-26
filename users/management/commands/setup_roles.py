from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate the ServicePlan model with initial data'

    def handle(self, *args, **kwargs):
        admin_group, created = Group.objects.get_or_create(name='Admin')
        standard_user_group, created = Group.objects.get_or_create(name='Standard User')
        quest_group, created = Group.objects.get_or_create(name='Guest')



        change_virtualmachine = Permission.objects.get(codename='change_virtualmachine')
        add_virtualmachine = Permission.objects.get(codename='add_virtualmachine')
        delete_virtualmachine = Permission.objects.get(codename='delete_virtualmachine')
        view_virtualmachine = Permission.objects.get(codename='view_virtualmachine')
        can_change_vm_owner = Permission.objects.get(codename='can_change_vm_owner')
        view_serviceplan = Permission.objects.get(codename='view_serviceplan')


        admin_group.permissions.add(add_virtualmachine,
                                    change_virtualmachine,
                                    delete_virtualmachine,
                                    view_virtualmachine,
                                    can_change_vm_owner,
                                    view_serviceplan
                                    )
        self.stdout.write(self.style.SUCCESS("Finished Admin setup"))

        standard_user_group.permissions.add(add_virtualmachine,
                                    change_virtualmachine,
                                    delete_virtualmachine,
                                    view_virtualmachine,
                                    view_serviceplan
                                    )

        self.stdout.write(self.style.SUCCESS("Finished Standard user setup"))
        quest_group.permissions.add(
            view_serviceplan
        )
        
        self.stdout.write(self.style.SUCCESS("Finsished Guest setup"))