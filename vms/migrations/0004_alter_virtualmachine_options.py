# Generated by Django 5.1.1 on 2024-09-22 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vms', '0003_alter_virtualmachine_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='virtualmachine',
            options={'permissions': [('can_change_vm_owner', 'Move VMs between users')]},
        ),
    ]
