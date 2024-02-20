from django.contrib import admin

from workers.models import Worker

all_info = ('first_name',
            'last_name', 'date_of_birth', 'years_of_experience', 'skills', 'salary', 'formatted_orders', 'owner')


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = all_info
    search_fields = ('first_name', 'last_name', 'skills', 'owner__username')
    list_per_page = 15
    ordering = ('first_name',)

    readonly_fields = ('date_of_birth', 'salary', 'owner',)

    def formatted_orders(self, obj):
        return ', '.join([str(order) for order in obj.orders.all()])

    formatted_orders.short_description = 'Orders'
