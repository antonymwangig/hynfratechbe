from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

admin_group = Group.objects.create(name='Admin')
standard_user_group = Group.objects.create(name='Standard User')
quest_group = Group.objects.create(name='Guest')



change_virtualmachine = Permission.objects.get(codename='change_virtualmachine')
add_virtualmachine = Permission.objects.get(codename='add_virtualmachine')
delete_virtualmachine = Permission.objects.get(codename='delete_virtualmachine')
view_virtualmachine = Permission.objects.get(codename='view_virtualmachine')
can_change_vm_owner = Permission.objects.get(codename='can_change_vm_owner')


admin_group.permissions.add(add_virtualmachine,
                            change_virtualmachine,
                            delete_virtualmachine,
                            view_virtualmachine,
                            can_change_vm_owner
                            )


admin_group.permissions.add(add_virtualmachine,
                            change_virtualmachine,
                            delete_virtualmachine,
                            view_virtualmachine
                            )
