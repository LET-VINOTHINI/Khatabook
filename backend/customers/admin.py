from django.contrib import admin
from .models import Customer, LedgerEntry


class LedgerEntryInline(admin.TabularInline):
    model = LedgerEntry
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'business')
    search_fields = ('name', 'mobile')
    inlines = [LedgerEntryInline]


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('customer', 'type', 'amount', 'date')
    list_filter = ('type',)
