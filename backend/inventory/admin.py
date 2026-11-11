from django.contrib import admin
from .models import InventoryItem


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'price', 'qty', 'low_stock_threshold')
    search_fields = ('name',)
