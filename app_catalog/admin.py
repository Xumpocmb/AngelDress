from django.contrib import admin

from .models import Dress, DressImage, DressCategory


class DressImageInline(admin.TabularInline):
    model = DressImage
    extra = 1
    readonly_fields = ['image_tag']
    fields = ('image', 'image_tag', 'order', 'alt_text')


@admin.register(Dress)
class DressAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'color', 'length', 'price_min', 'created_at')
    list_filter = ('category', 'color', 'length', 'fit')
    search_fields = ('name', 'description')
    inlines = [DressImageInline]
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'description', 'color', 'length', 'available_sizes')
        }),
        ('Детали', {
            'fields': ('fastener_type', 'fit', 'details', 'price_min', 'price_max')
        }),
        ('Рейтинг популярности', {
            'fields': ('views_count', 'favorites_count', 'popularity_score')
        }),
    )
    readonly_fields = ('views_count', 'favorites_count', 'popularity_score')


@admin.register(DressImage)
class DressImageAdmin(admin.ModelAdmin):
    list_display = ('dress', 'image_tag', 'order')
    list_editable = ('order',)
    list_filter = ('dress',)
    search_fields = ('dress__name', 'alt_text')


@admin.register(DressCategory)
class DressCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}