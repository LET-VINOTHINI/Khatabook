from rest_framework import viewsets, permissions

from .models import Bill
from .serializers import BillSerializer
from business.permissions import get_user_businesses


class BillViewSet(viewsets.ModelViewSet):
    serializer_class = BillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_business(self):
        return get_user_businesses(self.request.user).get(pk=self.kwargs['business_pk'])

    def get_queryset(self):
        return Bill.objects.filter(business=self.get_business()).prefetch_related('items')

    def perform_create(self, serializer):
        serializer.save(business=self.get_business())
