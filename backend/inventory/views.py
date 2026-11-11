from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import InventoryItem
from .serializers import InventoryItemSerializer
from business.permissions import get_user_businesses


class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_business(self):
        return get_user_businesses(self.request.user).get(pk=self.kwargs['business_pk'])

    def get_queryset(self):
        return InventoryItem.objects.filter(business=self.get_business())

    def perform_create(self, serializer):
        serializer.save(business=self.get_business())

    @action(detail=False, methods=['get'])
    def report(self, request, business_pk=None):
        items = list(self.get_queryset())
        low_stock = [i for i in items if i.is_low_stock]
        return Response({
            'items': InventoryItemSerializer(items, many=True).data,
            'low_stock_count': len(low_stock),
        })
