from rest_framework import serializers
from .models import Business, BusinessMembership


class BusinessSerializer(serializers.ModelSerializer):
    customer_count = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = ('id', 'name', 'type', 'upi_id', 'created_at', 'customer_count')
        read_only_fields = ('id', 'created_at')

    def get_customer_count(self, obj):
        return obj.customers.count()


class BusinessMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessMembership
        fields = ('id', 'business', 'name', 'mobile', 'role', 'can_add_entries', 'created_at')
        read_only_fields = ('id', 'business', 'created_at')
