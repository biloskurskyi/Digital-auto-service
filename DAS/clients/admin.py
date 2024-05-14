from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'owner',)
    search_fields = ('email', 'phone_number',)
    list_per_page = 15
    ordering = ('first_name',)
    readonly_fields = ('email', 'phone_number', 'owner',)
# Register your models here.
