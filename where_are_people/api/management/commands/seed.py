from api.models import User, Device, DeviceUser, Pings
from django.utils import timezone
from django.core.management.base import BaseCommand

import random


class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **options):
        seed_data()
        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))


def seed_data():

    Pings.objects.all().delete()
    DeviceUser.objects.all().delete()
    Device.objects.all().delete()
    User.objects.all().delete()

    user1, created = User.objects.get_or_create(username='alice', email='alice@example.com')
    user2, created = User.objects.get_or_create(username='bob', email='bob@example.com')

    device1, created = Device.objects.get_or_create(device_name='device1', ping_frequency=5)
    device2, created = Device.objects.get_or_create(device_name='device2', ping_frequency=10)

    DeviceUser.objects.get_or_create(device=device1, user=user1, defaults={'active': True})
    DeviceUser.objects.get_or_create(device=device2, user=user2, defaults={'active': True})

    for _ in range(5):
        Pings.objects.create(
            device=device1,
            user=user1,
            timestamp=timezone.now(),
            longitude=random.uniform(-180, 180),
            latitude=random.uniform(-90, 90)
        )
        Pings.objects.create(
            device=device2,
            user=user2,
            timestamp=timezone.now(),
            longitude=random.uniform(-180, 180),
            latitude=random.uniform(-90, 90)
        )

    print("Seed data created successfully.")
