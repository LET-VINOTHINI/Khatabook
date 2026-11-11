from rest_framework import serializers
from .models import Customer, LedgerEntry
from .services import customer_totals


class LedgerEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerEntry
        fields = ('id', 'customer', 'type', 'amount', 'note', 'date', 'created_at')
        read_only_fields = ('id', 'customer', 'created_at')


class CustomerSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    total_given = serializers.SerializerMethodField()
    total_received = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
            'id', 'business', 'name', 'mobile', 'created_at',
            'balance', 'total_given', 'total_received',
        )
        read_only_fields = ('id', 'business', 'created_at')

    def get_totals(self, obj):
        if not hasattr(obj, '_totals_cache'):
            obj._totals_cache = customer_totals(obj)
        return obj._totals_cache

    def get_balance(self, obj):
        return self.get_totals(obj)['balance']

    def get_total_given(self, obj):
        return self.get_totals(obj)['given']

    def get_total_received(self, obj):
        return self.get_totals(obj)['received']


class CustomerStatementSerializer(serializers.Serializer):
    customer = CustomerSerializer()
    entries = LedgerEntrySerializer(many=True)
    totals = serializers.DictField()
