from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import AccountUsers


@admin.register(AccountUsers)
class AccountUsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active',)
    search_fields = ('email',)
    list_per_page = 15
    ordering = ('username',)
    readonly_fields = ('password',)

    class Meta:
        verbose_name = 'Account User'
        verbose_name_plural = 'Account Users'

#
# UserAdmin.list_display = ('email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')
#
# admin.site.register(AccountUsers, UserAdmin)

# class CustomUserAdmin(UserAdmin):
#     # Customize the user admin as needed
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
#
#
# admin.site.register(AccountUsers, CustomUserAdmin)
