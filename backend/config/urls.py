from django.contrib import admin
from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from business.views import BusinessViewSet, BusinessMembershipViewSet
from customers.views import CustomerViewSet, LedgerEntryViewSet
from inventory.views import InventoryItemViewSet
from billing.views import BillViewSet
from devices.views import DeviceViewSet
from notifications.views import NotificationViewSet

router = DefaultRouter()
router.register('businesses', BusinessViewSet, basename='business')
router.register('devices', DeviceViewSet, basename='device')
router.register('notifications', NotificationViewSet, basename='notification')

business_router = NestedDefaultRouter(router, 'businesses', lookup='business')
business_router.register('staff', BusinessMembershipViewSet, basename='business-staff')
business_router.register('customers', CustomerViewSet, basename='business-customers')
business_router.register('inventory', InventoryItemViewSet, basename='business-inventory')
business_router.register('bills', BillViewSet, basename='business-bills')

customer_router = NestedDefaultRouter(business_router, 'customers', lookup='customer')
customer_router.register('entries', LedgerEntryViewSet, basename='customer-entries')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include(router.urls)),
    path('api/', include(business_router.urls)),
    path('api/', include(customer_router.urls)),
]
