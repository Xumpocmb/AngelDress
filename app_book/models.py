from app_catalog.models import Dress

from django.db import models


class RentalRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая заявка'),
        ('processed', 'Обработана'),
        ('rejected', 'Отклонена'),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя и фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    dresses = models.ManyToManyField(Dress, verbose_name='Платья')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус заявки'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    notes = models.TextField(blank=True, verbose_name='Примечания')

    class Meta:
        verbose_name = 'Заявка на примерку'
        verbose_name_plural = 'Заявки на примерку'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка #{self.id} от {self.name}"