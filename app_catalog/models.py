from email.mime import image
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.core.files.storage import default_storage
from django.utils.text import slugify
import magic


class DressCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='url', null=False, blank=False)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    image = models.ImageField(upload_to='dress_category/', verbose_name='Изображение', blank=True, null=True)
    show_on_main_page = models.BooleanField(default=True, verbose_name='Показывать на главной странице')

    def get_absolute_url(self):
        return reverse("app_catalog:dress_catalog")

    class Meta:
        verbose_name = 'Категория платья'
        verbose_name_plural = 'Категории платьев'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Dress(models.Model):
    category = models.ForeignKey(DressCategory, verbose_name='Категория', on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    color = models.CharField(blank=True, null=True, max_length=100, verbose_name="Цвет")
    length_choices = [
        ('mini', 'Мини'),
        ('midi', 'Миди (до колена)'),
        ('maxi', 'Макси (до пола)'),
    ]
    length = models.CharField(max_length=50, choices=length_choices, verbose_name='Длина')
    fastener_type = models.CharField(max_length=100, verbose_name='Тип застёжки', blank=True, null=True)
    fit_choices = [
        ('tight', 'Облегающий'),
        ('fitted', 'Приталенный'),
        ('loose', 'Свободный'),
    ]
    fit = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        choices=fit_choices,
        verbose_name="Посадка",
    )
    details = models.TextField(blank=True, null=True, verbose_name='Детали', help_text='Перечислите детали через запятую')
    rental_period = models.PositiveIntegerField(default=3, verbose_name='Срок аренды (дней)')
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость аренды', null=False, blank=False, default=0)
    pledge_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Залог', null=False, blank=False, default=0)
    available_sizes = models.CharField(max_length=200, verbose_name='Доступные размеры', help_text='Укажите размеры через дефис: XS-L')

    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    favorites_count = models.PositiveIntegerField(default=0, verbose_name='Количество избранных')
    popularity_score = models.FloatField(default=0.0, verbose_name='Рейтинг популярности', blank=True, null=True)

    class Meta:
        verbose_name = 'Платье'
        verbose_name_plural = 'Платья'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_details_list(self):
        return [d.strip() for d in self.details.split(',') if d.strip()]

    def get_sizes_list(self):
        return [s.strip() for s in self.available_sizes.split(',') if s.strip()]

    def update_popularity(self):
        self.popularity_score = self.views_count * 0.3 + self.favorites_count * 0.7
        self.save()

    def get_absolute_url(self):
        return reverse('app_catalog:dress_detail', args=[self.id])


class DressImage(models.Model):
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE, related_name='images', verbose_name='Платье')
    image = models.ImageField(upload_to='dresses/', verbose_name='Фотография')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Альтернативный текст')

    class Meta:
        verbose_name = 'Фотография платья'
        verbose_name_plural = 'Фотографии платьев'
        ordering = ['order']

    def __str__(self):
        return f"Фото {self.id} для {self.dress.name}"

    def delete(self, *args, **kwargs):
        if self.image:
            if default_storage.exists(self.image.name):
                default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)


class DressVideo(models.Model):
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="dresses/videos/", verbose_name="Видео")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    class Meta:
        ordering = ["order"]
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def __str__(self):
        return f"Видео для {self.dress.name}"

    def clean(self):
        if self.video:
            # Проверяем реальный тип файла по содержимому
            file_type = magic.from_buffer(self.video.read(1024), mime=True)
            if not file_type.startswith('video/'):
                raise ValidationError("Файл должен быть видео.")
            self.video.seek(0)

    def delete(self, *args, **kwargs):
        self.video.delete(save=False)
        super().delete(*args, **kwargs)
