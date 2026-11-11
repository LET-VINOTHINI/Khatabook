from django.contrib import admin
from .models import Bill, BillItem


class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 0


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'business', 'customer', 'gst_percent', 'created_at')
    inlines = [BillItemInline]
