from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)


class Device(models.Model):
    device_name = models.CharField(max_length=50)
    ping_frequency = models.IntegerField(default=10) # minutes


class DeviceUser(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('device', 'user')


class Pings(models.Model):
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now_add=True)
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=['device', '-timestamp']),
        ]

