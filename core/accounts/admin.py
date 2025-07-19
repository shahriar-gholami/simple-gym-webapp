from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('phone_number', 'full_name', 'is_active', 'is_staff', 'is_superuser', 'is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified', 'is_customer', 'is_shopowner')
    search_fields = ('phone_number', 'full_name')
    ordering = ('-created_date',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'otp_token')}),
        ('Permissions', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'is_customer', 'is_shopowner', 'groups', 'user_permissions')}),
        
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'full_name', 'email', 'is_active', 'is_verified', 'is_staff', 'is_superuser', 'is_customer', 'is_shopowner'),
        }),
    )

admin.site.register(User, UserAdmin)