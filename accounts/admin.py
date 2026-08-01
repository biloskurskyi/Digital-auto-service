from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import EmailVerification, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active', 'owner', 'is_superuser',
    )
    search_fields = ('email',)
    ordering = ('username',)
    list_per_page = 15
    readonly_fields = ('owner',)
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Tenant', {'fields': ('phone_number', 'owner', 'is_verified_email')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'phone_number', 'password1', 'password2')}),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expires_at')
    readonly_fields = ('created_at',)
