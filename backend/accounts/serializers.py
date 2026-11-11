from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)
    business_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    business_type = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('mobile', 'name', 'password', 'business_name', 'business_type')

    def validate_mobile(self, value):
        if User.objects.filter(mobile=value).exists():
            raise serializers.ValidationError('An account with this mobile number already exists.')
        return value

    def create(self, validated_data):
        from business.models import Business, BusinessMembership

        business_name = validated_data.pop('business_name', '') or 'My Business'
        business_type = validated_data.pop('business_type', '')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)

        business = Business.objects.create(owner=user, name=business_name, type=business_type)
        BusinessMembership.objects.create(
            business=business, user=user, name=user.name or user.mobile,
            mobile=user.mobile, role='owner', can_add_entries=True
        )
        user.current_business = business
        user.save(update_fields=['current_business'])
        return user


class UserSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(write_only=True, required=False, allow_blank=True)
    has_pin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'mobile', 'name', 'language', 'app_lock', 'pin', 'has_pin',
            'auto_backup', 'last_backup_at', 'current_business',
        )
        read_only_fields = ('id', 'mobile', 'last_backup_at')

    def get_has_pin(self, obj):
        return bool(obj.pin_hash)

    def update(self, instance, validated_data):
        pin = validated_data.pop('pin', None)
        if pin:
            instance.pin_hash = make_password(pin)
        return super().update(instance, validated_data)
