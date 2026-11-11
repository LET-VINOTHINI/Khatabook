from rest_framework import serializers
from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'device_token', 'last_active', 'is_current', 'created_at')
        read_only_fields = ('id', 'last_active', 'created_at')
