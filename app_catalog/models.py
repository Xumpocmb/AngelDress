from django.db import models
from django.utils import timezone
from django.core.files.storage import default_storage


class DressCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория платья'
        verbose_name_plural = 'Категории платьев'

    def __str__(self):
        return self.name


class Dress(models.Model):
    category = models.ForeignKey(DressCategory, verbose_name='Категория', on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    color = models.CharField(max_length=100, verbose_name='Цвет')
    length_choices = [
        ('mini', 'Мини'),
        ('midi', 'Миди (до колена)'),
        ('maxi', 'Макси (до пола)'),
    ]
    length = models.CharField(max_length=50, choices=length_choices, verbose_name='Длина')
    fastener_type = models.CharField(max_length=100, verbose_name='Тип застёжки')
    fit_choices = [
        ('tight', 'Облегающий'),
        ('fitted', 'Приталенный'),
        ('loose', 'Свободный'),
    ]
    fit = models.CharField(max_length=50, choices=fit_choices, verbose_name='Посадка')
    details = models.TextField(verbose_name='Детали', help_text='Перечислите детали через запятую')
    price_min = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Минимальная цена')
    price_max = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Максимальная цена')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    available_sizes = models.CharField(max_length=200, verbose_name='Доступные размеры',
                                       help_text='Перечислите размеры через запятую, например: XS,S,M,L')

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
        # Удаляем файл изображения при удалении записи
        if self.image:
            if default_storage.exists(self.image.name):
                default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)

    def image_tag(self):
        from django.utils.html import mark_safe
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" />')
        return "Нет изображения"

    image_tag.short_description = 'Предпросмотр'