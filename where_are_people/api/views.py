from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import OuterRef, Subquery
import random

from .models import User, Device, DeviceUser, Pings
from .serializers import UserSerializer, DeviceSerializer, PingsSerializer


@api_view(['POST', 'GET'])
def user(request):

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def add_device(request):

    if request.method == 'POST':
        serializer = DeviceSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def register_user_to_device(request, device_id):
    user_id = request.data['user_id']

    if not Device.objects.filter(id=device_id).exists():
        return Response(
            {'error': 'Device not found'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not User.objects.filter(id=user_id).exists():
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        device_user = DeviceUser.objects.get(device_id=device_id, user_id=user_id)
        device_user.active = True
        device_user.save()
    except DeviceUser.DoesNotExist:
        device_user = DeviceUser.objects.create(user_id=user_id, device_id=device_id, active=True)

    response_data = {
        'id': device_user.id,
        'device_id': device_user.device_id,
        'user_id': device_user.user_id,
        'active': device_user.active
    }
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def unregister_user_to_device(request, device_id):
    user_id = request.data['user_id']

    device_user = DeviceUser.objects.get(device_id=device_id,user_id=user_id)

    if device_user:
        device_user.active = False
        device_user.save()
        return Response(status=status.HTTP_200_OK)

    return Response(
        {"error": "Connection does not exist"},
        status=status.HTTP_404_NOT_FOUND
    )


@api_view(['GET'])
def get_location_device(request, device_id):

    device_user = DeviceUser.objects.filter(device_id=device_id, active=True).first()
    if not device_user:
        return Response({'error': 'No active device-user mapping found.'}, status=status.HTTP_404_NOT_FOUND)

    latitude = round(random.uniform(50.0, 54.0), 6)
    longitude = round(random.uniform(14.0, 24.0), 6)

    new_ping = Pings.objects.create(
        device_id=device_id,
        user=device_user.user,
        latitude=latitude,
        longitude=longitude
    )

    serialized_ping = PingsSerializer(new_ping)
    return Response(serialized_ping.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_last_location_user(request, user_id):

    ping = Pings.objects.filter(user_id=user_id).order_by('-timestamp').first()
    if not ping:
        return Response({'error': 'No location data found.'}, status=status.HTTP_404_NOT_FOUND)

    serialized_ping = PingsSerializer(ping)
    return Response(serialized_ping.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_location_devices(request):
    latest_pings_subquery = Pings.objects.filter(
        device=OuterRef('device')
    ).order_by('-timestamp')

    latest_pings = Pings.objects.filter(
        id__in=Subquery(latest_pings_subquery.values('id')[:1])
    )

    serializer = PingsSerializer(latest_pings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)









