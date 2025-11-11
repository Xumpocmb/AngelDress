from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .forms import ItemForm, AccessoryForm
from .models import (
    Item,
    ItemCategory,
    Accessory,
    AccessoryCategory,
    PriceOption,
    ItemImage,
    ItemVideo, Color, Size, Material, Brand, ItemCharacteristic, SuitableFor, FastenerType,
)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_preview')
    search_fields = ('name',)

    def color_preview(self, obj):
        if obj.hex_code:
            return format_html(
                '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ddd;"></div>',
                obj.hex_code
            )
        return "-"

    color_preview.short_description = "Цвет"


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'items_count')
    list_editable = ('order',)
    ordering = ('order',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            items_count=Count('item')
        )

    def items_count(self, obj):
        return obj.items_count

    items_count.admin_order_field = 'items_count'


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'items_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            items_count=Count('item')
        )

    def items_count(self, obj):
        return obj.items_count

    items_count.admin_order_field = 'items_count'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'items_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            items_count=Count('item')
        )

    def items_count(self, obj):
        return obj.items_count

    items_count.admin_order_field = 'items_count'


class ItemCharacteristicInline(admin.StackedInline):
    model = ItemCharacteristic
    fieldsets = (
        (None, {
            'fields': (
                ('train', 'sleeve'),
                ('fit', 'length'),
                'price_range',
            )
        }),
        ('Дополнительные характеристики', {
            'classes': ('collapse',),
            'fields': (
                ('has_3d_embroidery', 'has_feathers'),
                ('has_stones', 'has_beads'),
                ('has_pearls', 'is_transparent'),
                'has_pleats',
            )
        }),
    )
    extra = 0


class PriceOptionInline(admin.TabularInline):
    model = PriceOption
    extra = 0
    fields = ("name", "rental_period_days", "price", "pledge", "is_active")
    can_delete = True
    verbose_name = "Вариант цены"
    verbose_name_plural = "Варианты цен"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "item":
            kwargs["queryset"] = Item.objects.all()
        elif db_field.name == "accessory":
            kwargs["queryset"] = Accessory.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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


class ItemSizeInline(admin.TabularInline):
    model = Item.available_sizes.through
    extra = 1
    verbose_name = "Доступный размер"
    verbose_name_plural = "Доступные размеры"


class ItemColorInline(admin.TabularInline):
    model = Item.colors.through
    extra = 1
    verbose_name = "Цвет"
    verbose_name_plural = "Цвета"


class ItemMaterialInline(admin.TabularInline):
    model = Item.materials.through
    extra = 1
    verbose_name = "Материал"
    verbose_name_plural = "Материалы"


@admin.register(SuitableFor)
class SuitableForAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(FastenerType)
class FastenerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    list_display = (
        "thumbnail_preview",
        'name',
        'brand',
        'min_price',
        'is_active',
        'display_out_of_order',
        'created_at',
        'views_count',
        'colors_list',
        'sizes_list'
    )
    list_filter = (
        'is_active',
        'display_out_of_order',
        'brand',
        'categories',
        'created_at',
    )
    search_fields = (
        'name',
        'description',
        'brand__name',
    )
    filter_horizontal = (
        'categories',
        "colors",
        "materials",
        "available_sizes",
        "suitable_for", )
    readonly_fields = (
        'views_count',
        'favorites_count',
        'popularity_score',
        'created_at',
    )
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "is_active",
                    "display_out_of_order",
                    ("name", "brand", "article"),
                    "is_first_rental_promo",
                    "categories",
                    "suitable_for",
                    "description",
                    "details",
                    "fastener_type",
                    "min_price",
                )
            },
        ),
        (
            "Статистика",
            {
                "classes": ("collapse",),
                "fields": (
                    ("views_count", "favorites_count"),
                    "popularity_score",
                    "created_at",
                ),
            },
        ),
    )
    inlines = [
        ItemCharacteristicInline,
        ItemSizeInline,
        ItemColorInline,
        ItemMaterialInline,
        PriceOptionInline,
        ItemImageInline,
        ItemVideoInline,
    ]

    list_per_page = 50

    def colors_list(self, obj):
        return ", ".join([color.name for color in obj.colors.all()])

    colors_list.short_description = "Цвета"

    def sizes_list(self, obj):
        return ", ".join([size.name for size in obj.available_sizes.all()])

    sizes_list.short_description = "Размеры"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'colors',
            'available_sizes'
        ).select_related('brand')

    def thumbnail_preview(self, obj):
        if obj.get_first_image_url():
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.get_first_image_url(),
            )
        return ""

    thumbnail_preview.short_description = "Миниатюра"
    thumbnail_preview.allow_tags = True


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    form = AccessoryForm
    inlines = [PriceOptionInline, ItemImageInline, ItemVideoInline]
    list_display = (
        "thumbnail_preview",
        "name",
        "brand",
        "is_active",
        "display_out_of_order",
        "created_at",
    )
    list_editable = ("is_active",)
    list_filter = (
        "categories",
        "colors",
        "display_out_of_order",
    )
    search_fields = ("name", "description")
    filter_horizontal = ("categories",)

    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "categories",
                    ("name", "brand", "article"),
                    "description",
                    "is_active",
                    "display_out_of_order",
                )
            },
        ),
        (
            "Детали",
            {
                "fields": (
                    "colors",
                    "details",
                )
            },
        ),
        (
            "Рейтинг популярности",
            {"fields": ("views_count", "favorites_count", "popularity_score")},
        ),
    )
    readonly_fields = ("views_count", "favorites_count", "popularity_score")

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
    list_display = ("name", "items_count", "show_on_main_page", "is_active")
    search_fields = ("name",)
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_editable = (
        "is_active",
        "show_on_main_page",
    )

    def items_count(self, obj):
        return obj.items.count()

    items_count.short_description = "Количество"


@admin.register(AccessoryCategory)
class AccessoryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "accessories_count", "show_on_main_page", "is_active")
    search_fields = ("name",)
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_editable = (
        "is_active",
        "show_on_main_page",
    )

    def accessories_count(self, obj):
        return obj.accessories.count()

    accessories_count.short_description = "Количество"
