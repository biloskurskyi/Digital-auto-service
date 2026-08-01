from django.contrib import admin

from .models import Station


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'owner')
    search_fields = ('name', 'address', 'owner__username')
    list_per_page = 15
    ordering = ('name',)
    readonly_fields = ('name', 'address', 'owner')
