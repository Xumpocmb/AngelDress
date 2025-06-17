from django.db import models
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage


class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider/')
    alt_text = models.CharField(max_length=100, blank=True, verbose_name='Альтернативный текст')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Изображение слайдера'
        verbose_name_plural = 'Изображения слайдера'
        ordering = ['order']

    def __str__(self):
        return f"Слайд {self.id}"

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" />')
        return "Нет изображения"

    image_tag.short_description = 'Предпросмотр'

    def delete(self, *args, **kwargs):
        # Удаляем файл изображения при удалении записи
        if self.image:
            if default_storage.exists(self.image.name):
                default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)