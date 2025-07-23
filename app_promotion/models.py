from django.db import models
from django.core.files.storage import default_storage
from django.utils import timezone


class Promotion(models.Model):
    title = models.CharField('Название акции', max_length=100)
    description = models.TextField('Описание акции')
    image = models.ImageField(upload_to='promotions/')
    start_date = models.DateField('Дата начала', null=True, blank=True)
    end_date = models.DateField('Дата окончания', null=True, blank=True)
    is_active = models.BooleanField('Активна', default=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        ordering = ['order', '-start_date']

    def __str__(self):
        return self.title

    def short_description(self):
        """Возвращает сокращенное описание (до 100 символов)"""
        if len(self.description) > 100:
            return self.description[:97] + '...'
        return self.description

    def is_currently_active(self):
        """Проверяет, активна ли акция в текущий момент времени"""
        if not self.is_active:
            return False

        now = timezone.now().date()
        if self.start_date and self.end_date:
            return self.start_date <= now <= self.end_date
        if self.start_date:
            return now >= self.start_date
        if self.end_date:
            return now <= self.end_date
        return True

    is_currently_active.boolean = True
    is_currently_active.short_description = 'Активна сейчас'

    def get_date_range_display(self):
        """Форматирует период акции для отображения"""
        if self.start_date and self.end_date:
            return f"{self.start_date.strftime('%d.%m.%Y')} — {self.end_date.strftime('%d.%m.%Y')}"
        if self.start_date:
            return f"С {self.start_date.strftime('%d.%m.%Y')}"
        if self.end_date:
            return f"До {self.end_date.strftime('%d.%m.%Y')}"
        return ""

    def delete(self, *args, **kwargs):
        if self.image and default_storage.exists(self.image.name):
            default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)
