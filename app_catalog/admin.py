from django.contrib import admin

from django.contrib import admin
from .models import Dress, DressImage
from django.utils.html import format_html

class DressImageInline(admin.TabularInline):
    model = DressImage
    extra = 1
    readonly_fields = ['image_tag']
    fields = ('image', 'image_tag', 'order', 'alt_text')

@admin.register(Dress)
class DressAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'length', 'price_min', 'created_at')
    list_filter = ('color', 'length', 'fit')
    search_fields = ('name', 'description')
    inlines = [DressImageInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'color', 'length', 'available_sizes')
        }),
        ('Детали', {
            'fields': ('fastener_type', 'fit', 'details', 'price_min', 'price_max')
        }),
    )

@admin.register(DressImage)
class DressImageAdmin(admin.ModelAdmin):
    list_display = ('dress', 'image_tag', 'order')
    list_editable = ('order',)
    list_filter = ('dress',)
    search_fields = ('dress__name', 'alt_text')
