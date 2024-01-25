from django.contrib import admin

from accounts.models import AccountUsers

all_info = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active', 'owner')


@admin.register(AccountUsers)
class AccountUserAdmin(admin.ModelAdmin):
    list_display = all_info
    search_fields = ('email',)
    list_per_page = 15
    ordering = ('username',)
    readonly_fields = ('password',)
    sorted_fields = all_info

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            kwargs['queryset'] = AccountUsers.objects.filter(owner__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    actions = ['owners']

    def get_search_results(self, request, queryset, search_term):
        self.search_term = search_term
        return super().get_search_results(request, queryset, search_term)

    def owners(self, request, queryset):
        queryset, use_distinct = super().get_search_results(request, queryset, self.search_term)
        queryset = queryset.filter(owner__isnull=True)
        self.message_user(request, f'{len(queryset)} users were set as owners.')
        return queryset, use_distinct

    # def owners(self, request, queryset, search_term):
    #     queryset, use_distinct = super().get_search_results(request, queryset, search_term)
    #     queryset = queryset.filter(owner__isnull=True)
    #     return queryset, use_distinct

    # def filter_by_owner_null(self, request, queryset):
    #     search_term = request.POST.get('q', '')  # assuming 'q' is the search parameter
    #     queryset, use_distinct = self.get_search_results(request, queryset, search_term)
    #     queryset = queryset.filter(owner__isnull=True)
    #     return queryset, use_distinct
    #
    # filter_by_owner_null.short_description = "Owners"

    # actions = [get_search_results, ]

    # def owners(self, request, queryset):
    #     owners_list = queryset.filter(owner__isnull=True)
    #     return owners_list
    #
    # def managers(self, request, queryset):
    #     managers_list = queryset.filter(owner__isnull=False)
    #     return managers_list

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request).filter(owner__isnull=True)
    #     return queryset
    #
    # get_queryset.short_description = "Filter users with null owner"
    # actions = ['get_queryset']
