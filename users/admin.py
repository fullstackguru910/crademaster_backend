from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, IDFile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': (
            'email',
            'password',
            'wallet',
            'key',
            'cm_wallet',
            'cm_private_key',
            'cm_public_key',
            'cm_hex_address',
            'profit_percent',
            'referral_code',
            'referred_by',
            
        )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ['referral_code']
    list_display = ('email', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(IDFile)
