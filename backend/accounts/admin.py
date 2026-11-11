from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('mobile', 'name', 'is_staff', 'is_active')
    search_fields = ('mobile', 'name')
    ordering = ('mobile',)
    fieldsets = (
        (None, {'fields': ('mobile', 'password')}),
        ('Personal info', {'fields': ('name', 'language', 'app_lock', 'auto_backup', 'current_business')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'fields': ('mobile', 'password1', 'password2')}),
    )
