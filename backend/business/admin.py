from django.contrib import admin
from .models import Business, BusinessMembership


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'owner', 'created_at')
    search_fields = ('name', 'owner__mobile')


@admin.register(BusinessMembership)
class BusinessMembershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'role', 'mobile')
