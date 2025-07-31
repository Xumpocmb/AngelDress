import magic
from django.core.files.storage import default_storage
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class ItemCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(
        upload_to="dress_category/", verbose_name="Изображение", blank=True, null=True
    )
    is_active = models.BooleanField(default=False, verbose_name="Активна")
    show_on_main_page = models.BooleanField(
        default=True, verbose_name="Показывать на главной странице"
    )
    slug = models.SlugField(
        max_length=100, unique=True, verbose_name="url", null=False, blank=False
    )

    class Meta:
        db_table = "app_catalog_category"
        verbose_name = "Категория платья"
        verbose_name_plural = "Категории платьев"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("app_catalog:dress_catalog")


class Color(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название цвета")
    hex_code = models.CharField(max_length=7, blank=True, null=True, verbose_name="HEX-код")

    def __str__(self):
        return self.name

    def is_valid_hex(self):
        """Проверяет, является ли hex_code допустимым HEX цветом."""
        import re
        if not self.hex_code:
            return False
        # Проверка формата #XXX или #XXXXXX
        return bool(re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', self.hex_code))


class Size(models.Model):
    name = models.CharField(max_length=50, verbose_name="Размер")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название материала")

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название бренда")

    def __str__(self):
        return self.name


class SuitableFor(models.Model):
    name = models.CharField(max_length=100, verbose_name="Для кого подходит")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL", blank=True)

    class Meta:
        db_table = "app_catalog_suitable_for"
        verbose_name = "Для кого подходит"
        verbose_name_plural = "Для кого подходит"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FastenerType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип застёжки")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL", blank=True)

    class Meta:
        db_table = "app_catalog_fastener_type"
        verbose_name = "Тип застёжки"
        verbose_name_plural = "Типы застёжек"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ItemCharacteristic(models.Model):
    TRAIN_CHOICES = [
        ('without', 'Без шлейфа'),
        ('short', 'Короткий шлейф'),
        ('long', 'Длинный шлейф'),
    ]

    SLEEVE_CHOICES = [
        ('none', 'Без рукава'),
        ('short', 'Короткий рукав'),
        ('3_4', '3/4 рукава'),
        ('long', 'Длинный рукав'),
        ('one', 'Один рукав'),
        ('off_shoulder', 'Спущенные рукава (открытые плечи)'),
        ('removable', 'Съемный рукав'),
    ]

    FIT_CHOICES = [
        ('asymmetrical', 'Ассиметрия'),
        ('straight', 'Прямое'),
        ('fluffy', 'Пышное'),
        ('mermaid', 'Рыбка'),
    ]

    LENGTH_CHOICES = [
        ('mini', 'Мини'),
        ('midi', 'Миди'),
        ('maxi', 'Макси (в пол)'),
    ]

    PRICE_RANGE_CHOICES = [
        ('0-5000', 'до 5000'),
        ('5000-10000', '5000 - 10000'),
        ('6000-10000', '6000 - 10000'),
        ('10000-15000', '10000 - 15000'),
        ('15000-20000', '15000 - 20000'),
    ]

    item = models.OneToOneField(
        'Item',
        on_delete=models.CASCADE,
        related_name='characteristics',
        verbose_name="Товар"
    )

    train = models.CharField(
        max_length=20,
        choices=TRAIN_CHOICES,
        blank=True,
        null=True,
        verbose_name="Шлейф"
    )

    sleeve = models.CharField(
        max_length=20,
        choices=SLEEVE_CHOICES,
        blank=True,
        null=True,
        verbose_name="Рукав"
    )

    fit = models.CharField(
        max_length=20,
        choices=FIT_CHOICES,
        blank=True,
        null=True,
        verbose_name="Фасон"
    )

    length = models.CharField(
        max_length=20,
        choices=LENGTH_CHOICES,
        blank=True,
        null=True,
        verbose_name="Длина"
    )

    price_range = models.CharField(
        max_length=20,
        choices=PRICE_RANGE_CHOICES,
        blank=True,
        null=True,
        verbose_name="Цена на мероприятие"
    )

    has_3d_embroidery = models.BooleanField(default=False, verbose_name="3D вышивка")
    has_feathers = models.BooleanField(default=False, verbose_name="С перьями")
    has_stones = models.BooleanField(default=False, verbose_name="Платье в стразах")
    has_beads = models.BooleanField(default=False, verbose_name="Расшито бисером")
    has_pearls = models.BooleanField(default=False, verbose_name="Расшито жемчугом")
    is_transparent = models.BooleanField(default=False, verbose_name="Прозрачный")
    has_pleats = models.BooleanField(default=False, verbose_name="Плиссе")


class Item(models.Model):
    categories = models.ManyToManyField(
        ItemCategory,
        verbose_name="Категории",
        related_name="items"
    )
    # brand = models.ForeignKey(
    #     Brand,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     verbose_name="Бренд"
    # )
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )

    # colors = models.ManyToManyField(
    #     Color,
    #     verbose_name="Цвета",
    #     blank=True
    # )

    # materials = models.ManyToManyField(
    #     Material,
    #     verbose_name="Материалы",
    #     blank=True
    # )

    # available_sizes = models.ManyToManyField(
    #     Size,
    #     verbose_name="Доступные размеры",
    #     blank=True
    # )

    # fastener_type = models.ForeignKey(
    #     FastenerType,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     verbose_name="Тип застёжки"
    # )

    # details = models.TextField(
    #     blank=True,
    #     null=True,
    #     verbose_name="Детали",
    #     help_text="Перечислите детали через запятую",
    # )
    # suitable_for = models.ManyToManyField(
    #     SuitableFor,
    #     verbose_name="Для кого подходит",
    #     blank=True,
    #     related_name="items"
    # )

    is_first_rental_promo = models.BooleanField(
        default=False,
        verbose_name="Акция 'Первый прокат'",
        help_text="Если отмечено, на карточке товара будет отображаться значок акции 'первый прокат'."
    )

    is_active = models.BooleanField(default=True, verbose_name="Активен")

    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )
    favorites_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество избранных"
    )
    popularity_score = models.FloatField(
        default=0.0, verbose_name="Рейтинг популярности", blank=True, null=True
    )

    min_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Минимальная цена",
        help_text="Обновляется автоматически",
    )

    class Meta:
        db_table = "app_catalog_item"
        verbose_name = "Платье"
        verbose_name_plural = "Платья"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def update_popularity(self):
        self.popularity_score = self.views_count * 0.3 + self.favorites_count * 0.7
        self.save()

    def get_absolute_url(self):
        return reverse('app_catalog:item_detail', args=[self.id])

    def get_first_image_url(self):
        if self.images.exists():
            return self.images.first().image.url
        return "/static/img/No-Image-Placeholder.png"

    def update_min_price(self):
        """Обновляет min_price на основе активных PriceOption"""
        min_option = self.price_options.filter(is_active=True).order_by("price").first()
        if min_option:
            self.min_price = min_option.price
        else:
            self.min_price = None
        self.save(update_fields=["min_price"])


class AccessoryCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(
        upload_to="accessory_category/", verbose_name="Изображение", blank=True, null=True
    )
    is_active = models.BooleanField(default=False, verbose_name="Активна")
    show_on_main_page = models.BooleanField(
        default=True, verbose_name="Показывать на главной странице"
    )
    slug = models.SlugField(
        max_length=100, unique=True, verbose_name="url", null=False, blank=False
    )

    class Meta:
        db_table = "app_accessory_category"
        verbose_name = "Категория аксессуаров"
        verbose_name_plural = "Категории аксессуаров"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("app_catalog:accessory_catalog")


class Accessory(models.Model):
    categories = models.ManyToManyField(
        AccessoryCategory, verbose_name="Категории", related_name="accessories"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Бренд"
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    colors = models.ManyToManyField(
        Color, verbose_name="Цвета", blank=True
    )
    details = models.TextField(
        blank=True,
        null=True,
        verbose_name="Детали",
        help_text="Перечислите детали через запятую",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )
    favorites_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество избранных"
    )
    popularity_score = models.FloatField(
        default=0.0, verbose_name="Рейтинг популярности", blank=True, null=True
    )
    min_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Минимальная цена",
        help_text="Обновляется автоматически",
    )

    class Meta:
        db_table = "app_catalog_accessory"
        verbose_name = "Аксессуар"
        verbose_name_plural = "Аксессуары"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def update_popularity(self):
        self.popularity_score = self.views_count * 0.3 + self.favorites_count * 0.7
        self.save()

    def get_absolute_url(self):
        return reverse('app_catalog:accessory_detail', args=[self.id])

    def get_first_image_url(self):
        if self.images.exists():
            return self.images.first().image.url
        return "/static/img/No-Image-Placeholder.png"

    def update_min_price(self):
        min_option = self.price_options.filter(is_active=True).order_by("price").first()
        if min_option:
            self.min_price = min_option.price
        else:
            self.min_price = None
        self.save(update_fields=["min_price"])


class PriceOption(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="price_options",
        verbose_name="Платье",
        null=True,
        blank=True,
    )
    accessory = models.ForeignKey(
        Accessory,
        on_delete=models.CASCADE,
        related_name="price_options",
        verbose_name="Аксессуар",
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название опции",
        help_text='Пример: "Мероприятие", "Фотосессия"',
        default="Мероприятие",
    )
    rental_period_days = models.PositiveIntegerField(
        default=3, verbose_name="Срок аренды (дни)", null=True, blank=True
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Стоимость аренды", default=0
    )
    pledge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Залог",
        null=True,
        blank=True,
        default=0,
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        db_table = "app_catalog_price_option"
        verbose_name = "Вариант цены"
        verbose_name_plural = "Варианты цен"

    def __str__(self):
        return f"{self.name} - {self.price} ₽"


class ItemImage(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="images", verbose_name="Платье", null=True, blank=True
    )
    accessory = models.ForeignKey(
        Accessory, on_delete=models.CASCADE, related_name="images", verbose_name="Аксессуар", null=True, blank=True
    )
    image = models.ImageField(upload_to="dresses/", verbose_name="Фотография")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    alt_text = models.CharField(
        max_length=200, blank=True, verbose_name="Альтернативный текст"
    )

    class Meta:
        db_table = "app_catalog_item_image"
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"
        ordering = ["order"]

    def __str__(self):
        if self.item:
            return f"Фото {self.id} для {self.item.name}"
        elif self.accessory:
            return f"Фото {self.id} для {self.accessory.name}"
        return f"Фото {self.id} (без связи)"

    def delete(self, *args, **kwargs):
        if self.image:
            if default_storage.exists(self.image.name):
                default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)


class ItemVideo(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="videos", verbose_name="Платье", null=True, blank=True
    )
    accessory = models.ForeignKey(
        Accessory, on_delete=models.CASCADE, related_name="videos", verbose_name="Аксессуар", null=True, blank=True
    )
    video = models.FileField(upload_to="dresses/videos/", verbose_name="Видео")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    class Meta:
        db_table = "app_catalog_item_video"
        ordering = ["order"]
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def __str__(self):
        if self.item:
            return f"Видео {self.id} для {self.item.name}"
        elif self.accessory:
            return f"Видео {self.id} для {self.accessory.name}"
        return f"Видео {self.id} (без связи)"

    def clean(self):
        if self.video:
            # Проверяем реальный тип файла по содержимому
            file_type = magic.from_buffer(self.video.read(1024), mime=True)
            if not file_type.startswith("video/"):
                raise ValidationError("Файл должен быть видео.")
            self.video.seek(0)

    def delete(self, *args, **kwargs):
        self.video.delete(save=False)
        super().delete(*args, **kwargs)
