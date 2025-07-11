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
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("app_catalog:dress_catalog")


class Item(models.Model):
    length_choices = [
        ("mini", "Мини"),
        ("midi", "Миди"),
        ("maxi", "Макси"),
    ]
    fit_choices = [
        ("tight", "Облегающий"),
        ("fitted", "Приталенный"),
        ("loose", "Свободный"),
    ]
    categories = models.ManyToManyField(
        ItemCategory, verbose_name="Категории", related_name="items"
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )

    color = models.CharField(blank=True, null=True, max_length=100, verbose_name="Цвет")
    length = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        choices=length_choices,
        verbose_name="Длина",
    )
    fastener_type = models.CharField(
        blank=True, null=True, max_length=100, verbose_name="Тип застёжки"
    )
    fit = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        choices=fit_choices,
        verbose_name="Посадка",
    )
    details = models.TextField(
        blank=True,
        null=True,
        verbose_name="Детали",
        help_text="Перечислите детали через запятую",
    )
    available_sizes = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        verbose_name="Доступные размеры",
        help_text="Укажите размеры через дефис: XS-L",
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
        verbose_name = "Товары"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def update_popularity(self):
        self.popularity_score = self.views_count * 0.3 + self.favorites_count * 0.7
        self.save()

    def get_absolute_url(self):
        return reverse("app_catalog:dress_detail", args=[self.id])

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


class PriceOption(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="price_options",
        verbose_name="Платье",
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
        Item, on_delete=models.CASCADE, related_name="images", verbose_name="Товар"
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
        return f"Фото {self.id} для {self.item.name}"

    def delete(self, *args, **kwargs):
        if self.image:
            if default_storage.exists(self.image.name):
                default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)


class ItemVideo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="dresses/videos/", verbose_name="Видео")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    class Meta:
        db_table = "app_catalog_item_video"
        ordering = ["order"]
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def __str__(self):
        return f"Видео для {self.item.name}"

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
