from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'car', 'start_date', 'process_status', 'info')
    search_fields = ('client__first_name', 'client__last_name', 'car__car_number')
    list_per_page = 15
    readonly_fields = ('client', 'car',)
# Register your models here.
