from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import AccountUsers
from stations.models import Station

all_info = ('name', 'address', 'owner',)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = all_info
    search_fields = all_info
    list_per_page = 15
    ordering = ('name',)
    readonly_fields = all_info
    # sorted_fields = ('is_superuser',)
