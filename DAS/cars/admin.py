from django.contrib import admin

from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('client',
                    'car_number', 'vin_number', 'mark', 'model', 'year', 'engine', 'gear_type', 'short_comment',)
    search_fields = ('car_number',)
    list_per_page = 15
    ordering = ('client',)
    readonly_fields = ('client', 'car_number', 'vin_number', 'mark', 'model', 'year', 'engine', 'gear_type',)

    def short_comment(self, obj):
        if len(obj.comment) > 15:
            return obj.comment[:15] + '...'
        else:
            return obj.comment

    short_comment.short_description = 'comment'  # Set the column name in admin panel
