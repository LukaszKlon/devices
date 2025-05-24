from rest_framework import serializers
from .models import User, Device, DeviceUser, Pings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class DeviceUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    device = DeviceSerializer()

    class Meta:
        model = DeviceUser
        fields = '__all__'


class PingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pings
        fields = '__all__'

