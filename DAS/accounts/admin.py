from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import AccountUsers

all_info = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active', 'owner', 'is_superuser')

admin.site.register(AccountUsers, UserAdmin)


# @admin.register(AccountUsers)
class AccountUserAdmin(admin.ModelAdmin):
    list_display = all_info
    search_fields = ('email',)
    list_per_page = 15
    ordering = ('username',)
    readonly_fields = ('password',)
    sorted_fields = ('is_superuser',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            kwargs['queryset'] = AccountUsers.objects.filter(owner__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    actions = ['owners', ]

    # def get_search_results(self, request, queryset, search_term):
    #     self.search_term = search_term
    #     return super().get_search_results(request, queryset, search_term)

    def owners(self, request, queryset):
        queryset, use_distinct = super().get_search_results(request, queryset, self.search_term)
        queryset = queryset.filter(owner__isnull=True)
        self.message_user(request, f'{len(queryset)} users were set as owners.')
        return queryset, use_distinct
