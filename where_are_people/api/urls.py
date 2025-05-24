from django.urls import path
from . import views

urlpatterns = [
    path('users', views.user),
    path('devices', views.add_device),
    path('devices/<int:device_id>/assign/', views.register_user_to_device),
    path('devices/<int:device_id>/unassign/', views.unregister_user_to_device),
    path('devices/<int:device_id>/location/', views.get_location_device),
    path('users/<int:user_id>/location/', views.get_last_location_user),
    path('map/', views.get_all_location_devices),
]