from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import AccountUsers


@admin.register(AccountUsers)
class KeyPointsAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active',)
    search_fields = ('email',)
    list_per_page = 15
    ordering = ('username',)
    readonly_fields = ('password',)

    class Meta:
        verbose_name = 'Account users'
