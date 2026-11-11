from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Customer, LedgerEntry
from .serializers import CustomerSerializer, LedgerEntrySerializer
from .services import customer_totals
from business.permissions import get_user_businesses


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_business(self):
        business_id = self.kwargs['business_pk']
        return get_user_businesses(self.request.user).get(pk=business_id)

    def get_queryset(self):
        q = self.request.query_params.get('q', '').strip()
        qs = Customer.objects.filter(business=self.get_business())
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(mobile__icontains=q)
        return qs

    def perform_create(self, serializer):
        serializer.save(business=self.get_business())

    @action(detail=True, methods=['get'])
    def statement(self, request, business_pk=None, pk=None):
        customer = self.get_object()
        entries = customer.entries.all()
        return Response({
            'customer': CustomerSerializer(customer).data,
            'entries': LedgerEntrySerializer(entries, many=True).data,
            'totals': customer_totals(customer),
        })


class LedgerEntryViewSet(viewsets.ModelViewSet):
    serializer_class = LedgerEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_customer(self):
        business = get_user_businesses(self.request.user).get(pk=self.kwargs['business_pk'])
        return Customer.objects.get(pk=self.kwargs['customer_pk'], business=business)

    def get_queryset(self):
        return LedgerEntry.objects.filter(customer=self.get_customer())

    def perform_create(self, serializer):
        serializer.save(customer=self.get_customer())
