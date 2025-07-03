from django.db import models
from app_catalog.models import Item


class RentalRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "Не обработана"),
        ("accepted", "Принята"),
        ("processing", "В процессе"),
        ("done", "Обработана"),
        ("rejected", "Отклонена"),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя и фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    items = models.ManyToManyField(Item, verbose_name='Товары', help_text='Кликните, чтобы выбрать товары, которые интересуют клиента /')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус заявки'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    notes = models.TextField(blank=True, verbose_name='Примечания', null=True)

    class Meta:
        verbose_name = 'Заявка на примерку'
        verbose_name_plural = 'Заявки на примерку'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка #{self.id} от {self.name}"
