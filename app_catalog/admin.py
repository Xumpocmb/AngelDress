from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Dress, DressImage, DressCategory, DressVideo


class DressImageInline(admin.TabularInline):
    model = DressImage
    extra = 1
    readonly_fields = ["image_tag"]
    fields = ("image", "image_tag", "order", "alt_text")

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return "Нет изображения"

    image_tag.short_description = "Предпросмотр"


class DressVideoInline(admin.TabularInline):
    model = DressVideo
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


@admin.register(Dress)
class DressAdmin(admin.ModelAdmin):
    list_display = ("category", "name", "color", "length", "rental_price", "created_at")
    list_filter = ("category", "color", "length", "fit")
    search_fields = ("name", "description")
    inlines = [DressImageInline, DressVideoInline]
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "category",
                    "name",
                    "description",
                    "color",
                )
            },
        ),
        (
            "Детали",
            {
                "fields": (
                    "available_sizes",
                    "length",
                    "fastener_type",
                    "fit",
                    "details",
                )
            },
        ),
        (
            "Прокат",
            {
                "fields": (
                    "rental_period",
                    "rental_price",
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


@admin.register(DressCategory)
class DressCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}
