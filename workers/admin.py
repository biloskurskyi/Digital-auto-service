from django.contrib import admin

from .models import Worker


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'date_of_birth', 'years_of_experience', 'skills', 'salary',
        'formatted_orders', 'owner',
    )
    search_fields = ('first_name', 'last_name', 'skills', 'owner__username')
    list_per_page = 15
    ordering = ('first_name',)
    readonly_fields = ('date_of_birth', 'salary', 'owner')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('orders')

    @admin.display(description='Orders')
    def formatted_orders(self, obj):
        return ', '.join(str(order) for order in obj.orders.all())
