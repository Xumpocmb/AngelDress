from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    Item,
    ItemImage,
    ItemCategory,
    ItemVideo,
)


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    readonly_fields = ["image_tag"]
    fields = ("image", "image_tag", "order", "alt_text")

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return "Нет изображения"

    image_tag.short_description = "Предпросмотр"


class ItemVideoInline(admin.TabularInline):
    model = ItemVideo
    extra = 1
    readonly_fields = ("video_tag",)
    fields = ("video", "video_tag", "order", "alt_text")

    def video_tag(self, obj):
        if obj.video:
            return mark_safe(
                f'<video width="150" controls><source src="{obj.video.url}" type="video/mp4">Ваш браузер не поддерживает видео</video>'
            )
        return "Нет видео"

    video_tag.short_description = "Предпросмотр"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemImageInline, ItemVideoInline]
    list_display = (
        "thumbnail_preview",
        "name",
        "is_active",
        "created_at",
    )
    list_editable = ("is_active",)
    list_filter = (
        "categories",
        "color",
        "length",
        "fit",
    )
    search_fields = ("name", "description")
    filter_horizontal = ("categories",)

    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "categories",
                    "name",
                    "description",
                    "is_active",
                )
            },
        ),
        (
            "Детали",
            {
                "fields": (
                    "color",
                    "length",
                    "fastener_type",
                    "fit",
                    "details",
                    "available_sizes",
                )
            },
        ),
        (
            "Прокат",
            {
                "fields": (
                    "rental_period",
                    "rental_price",
                    "photoset_price",
                    "pledge_price",
                )
            },
        ),
        (
            "Рейтинг популярности",
            {"fields": ("views_count", "favorites_count", "popularity_score")},
        ),
    )
    readonly_fields = ("views_count", "favorites_count", "popularity_score")

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = "Категории"

    def thumbnail_preview(self, obj):
        if obj.get_first_image_url():
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.get_first_image_url(),
            )
        return ""

    thumbnail_preview.short_description = "Миниатюра"
    thumbnail_preview.allow_tags = True


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "items_count", "show_on_main_page",  "is_active")
    search_fields = ("name",)
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active", "show_on_main_page",)

    def items_count(self, obj):
        return obj.items.count()

    items_count.short_description = "Количество"

