# Generated by Django 5.1.1 on 2024-09-22 01:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualMachine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('state', models.CharField(choices=[('running', 'Running'), ('stopped', 'Stopped'), ('paused', 'Paused'), ('suspended', 'Suspended')], default='stopped', max_length=10)),
                ('vcpu_count', models.IntegerField(default=1)),
                ('memory_size', models.IntegerField(help_text='Memory size in MB')),
                ('disk_size', models.IntegerField(help_text='Disk size in GB')),
                ('mac_address', models.CharField(blank=True, max_length=17, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
