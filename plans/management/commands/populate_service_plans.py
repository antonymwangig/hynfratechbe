from django.core.management.base import BaseCommand
from your_app_name.models import ServicePlan

class Command(BaseCommand):
    help = 'Populate the ServicePlan model with initial data'

    def handle(self, *args, **kwargs):
        plans = [
            {
                "name": "Bronze",
                "price": "5",
                "features": ["1 Core", "512 MB RAM", "10 GB Storage", "500 GB Network Bandwidth", "Up to 2 backups/month"],
                "vcpu_count": 1,
                "memory_size": 512000,
                "disk_size": 10
            },
            {
                "name": "Silver",
                "price": "10",
                "features": ["2 Cores", "1 GB RAM", "50 GB Storage", "1 TB Network Bandwidth", "Up to 4 backups/month"],
                "vcpu_count": 2,
                "memory_size": 1024000,
                "disk_size": 50
            },
            {
                "name": "Gold",
                "price": "25",
                "features": ["4 Cores", "2 GB RAM", "200 GB Storage", "5 TB Network Bandwidth", "Up to 10 backups/month"],
                "vcpu_count": 4,
                "memory_size": 2048000,
                "disk_size": 200
            },
            {
                "name": "Platinum",
                "price": "60",
                "features": ["8 Cores", "4 GB RAM", "1 TB Storage", "Unlimited Bandwidth", "Unlimited backups/month"],
                "vcpu_count": 8,
                "memory_size": 4096000,
                "disk_size": 1024
            }
        ]

        for plan in plans:
            if not ServicePlan.objects.filter(name=plan['name']).exists():
                ServicePlan.objects.create(
                    name=plan['name'],
                    price=plan['price'],
                    features=plan['features'],
                    vcpu_count=plan['vcpu_count'],
                    memory_size=plan['memory_size'],
                    disk_size=plan['disk_size']
                )
                self.stdout.write(self.style.SUCCESS(f"Created plan: {plan['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Plan {plan['name']} already exists"))
