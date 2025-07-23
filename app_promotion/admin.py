from django.contrib import admin
from .models import Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_date_range_display', 'is_active', 'is_currently_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'is_active')
        }),
        ('Даты проведения', {
            'fields': ('start_date', 'end_date'),
            'description': 'Оставьте пустыми, если акция бессрочная',
            'classes': ('collapse',)
        }),
        ('Порядок отображения', {
            'fields': ('order',),
            'classes': ('collapse',)
        })
    )

    def get_date_range_display(self, obj):
        return obj.get_date_range_display()
    get_date_range_display.short_description = 'Период проведения'
