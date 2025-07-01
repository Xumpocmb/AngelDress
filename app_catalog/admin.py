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
    list_display = (
        "name",
        "display_categories",
        "color",
        "length",
        "rental_price",
        "created_at",
    )
    list_filter = (
        "categories",
        "color",
        "length",
        "fit",
    )  # Изменено с category на categories
    search_fields = ("name", "description")
    inlines = [DressImageInline, DressVideoInline]
    filter_horizontal = ("categories",)  # Добавлено для удобного выбора категорий

    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "categories",  # Изменено с category на categories
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

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    display_categories.short_description = (
        "Категории"  # Задаём читаемое название колонки
    )


@admin.register(DressCategory)
class DressCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "dress_count")  # Добавлено отображение количества платьев
    search_fields = ("name",)
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def dress_count(self, obj):
        return obj.dresses.count()  # Используем related_name='dresses'

    dress_count.short_description = "Количество платьев"
