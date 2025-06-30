from django.db import models


class ClientCallBack(models.Model):
    STATUS_CHOICES = [
        ("new", "Не обработана"),
        ("accepted", "Принята"),
        ("processing", "В процессе"),
        ("done", "Обработана"),
        ("rejected", "Отклонена"),
    ]

    name = models.CharField(max_length=255, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус"
    )
    description = models.TextField(blank=True, verbose_name="Заметки", null=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

    class Meta:
        verbose_name = "Заявка на обратный звонок"
        verbose_name_plural = "Заявки на обратный звонок"
