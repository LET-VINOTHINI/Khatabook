from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Business, BusinessMembership
from .serializers import BusinessSerializer, BusinessMembershipSerializer
from .permissions import get_user_businesses, get_user_role
from customers.services import business_totals, outstanding_summary
from customers.models import LedgerEntry


class BusinessViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_businesses(self.request.user)

    def perform_create(self, serializer):
        business = serializer.save(owner=self.request.user)
        BusinessMembership.objects.create(
            business=business, user=self.request.user,
            name=self.request.user.name or self.request.user.mobile,
            mobile=self.request.user.mobile, role='owner', can_add_entries=True,
        )
        if not self.request.user.current_business_id:
            self.request.user.current_business = business
            self.request.user.save(update_fields=['current_business'])

    def perform_update(self, serializer):
        if get_user_role(self.get_object(), self.request.user) != 'owner':
            raise permissions.PermissionDenied('Only the owner can edit this business.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner_id != self.request.user.id:
            raise permissions.PermissionDenied('Only the owner can delete this business.')
        instance.delete()

    @action(detail=True, methods=['post'])
    def switch(self, request, pk=None):
        business = self.get_object()
        request.user.current_business = business
        request.user.save(update_fields=['current_business'])
        return Response(BusinessSerializer(business).data)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        business = self.get_object()
        return Response(business_totals(business))

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        business = self.get_object()
        totals = business_totals(business)
        summary_rows = outstanding_summary(business)
        top_due = summary_rows[0] if summary_rows and summary_rows[0]['balance'] > 0 else None
        return Response({
            'customer_count': business.customers.count(),
            **totals,
            'top_due_customer': top_due,
        })

    @action(detail=True, methods=['get'])
    def outstanding_summary(self, request, pk=None):
        business = self.get_object()
        rows = outstanding_summary(business)
        total_due = sum((r['balance'] for r in rows if r['balance'] > 0), start=0)
        return Response({'rows': rows, 'total_due': total_due})

    @action(detail=True, methods=['get'], url_path='recent-entries')
    def recent_entries(self, request, pk=None):
        business = self.get_object()
        limit = int(request.query_params.get('limit', 10))
        entries = (
            LedgerEntry.objects.filter(customer__business=business)
            .select_related('customer')
            .order_by('-date', '-created_at')[:limit]
        )
        data = [{
            'id': e.id,
            'customer_id': e.customer_id,
            'customer_name': e.customer.name,
            'type': e.type,
            'amount': e.amount,
            'note': e.note,
            'date': e.date,
        } for e in entries]
        return Response(data)


class BusinessMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_business(self):
        business_id = self.kwargs['business_pk']
        return get_user_businesses(self.request.user).get(pk=business_id)

    def get_queryset(self):
        return BusinessMembership.objects.filter(business=self.get_business())

    def perform_create(self, serializer):
        serializer.save(business=self.get_business())

    def perform_update(self, serializer):
        if get_user_role(self.get_business(), self.request.user) != 'owner':
            raise permissions.PermissionDenied('Only the owner can manage staff.')
        serializer.save()

    def perform_destroy(self, instance):
        if get_user_role(self.get_business(), self.request.user) != 'owner':
            raise permissions.PermissionDenied('Only the owner can manage staff.')
        if instance.role == 'owner':
            raise permissions.PermissionDenied('Cannot remove the owner.')
        instance.delete()
