from rest_framework import serializers
from .models import InventoryItem


class InventoryItemSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.ReadOnlyField()

    class Meta:
        model = InventoryItem
        fields = (
            'id', 'business', 'name', 'price', 'qty',
            'low_stock_threshold', 'is_low_stock', 'created_at',
        )
        read_only_fields = ('id', 'business', 'created_at')
