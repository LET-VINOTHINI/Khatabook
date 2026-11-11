from rest_framework import serializers
from .models import Bill, BillItem


class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        fields = ('id', 'inventory_item', 'name', 'qty', 'price')
        read_only_fields = ('id',)


class BillSerializer(serializers.ModelSerializer):
    items = BillItemSerializer(many=True)
    subtotal = serializers.ReadOnlyField()
    tax_amount = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()

    class Meta:
        model = Bill
        fields = (
            'id', 'business', 'customer', 'gst_percent',
            'items', 'subtotal', 'tax_amount', 'total', 'created_at',
        )
        read_only_fields = ('id', 'business', 'created_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        bill = Bill.objects.create(**validated_data)
        for item_data in items_data:
            BillItem.objects.create(bill=bill, **item_data)
            inv_item = item_data.get('inventory_item')
            if inv_item:
                inv_item.qty = max(0, inv_item.qty - item_data['qty'])
                inv_item.save(update_fields=['qty'])
        return bill
