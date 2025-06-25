from django.db import models
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage


class SliderImage(models.Model):
    image = models.ImageField(upload_to="slider/")
    alt_text = models.CharField(
        max_length=100, blank=True, verbose_name="Альтернативный текст"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Изображение слайдера"
        verbose_name_plural = "Изображения слайдера"
        ordering = ["order"]

    def __str__(self):
        return f"Слайд {self.id}"

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" />')
        return "Нет изображения"

    image_tag.short_description = "Предпросмотр"

    def save(self, *args, **kwargs):
        # Удаляем старое изображение при обновлении
        if self.pk:  # Если объект уже существует в БД
            old_instance = SliderImage.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image != self.image:
                if default_storage.exists(old_instance.image.name):
                    default_storage.delete(old_instance.image.name)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удаляем файл изображения при удалении записи
        if self.image:
            if default_storage.exists(self.image.name):
                default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)


class ContactInfo(models.Model):
    address = models.CharField(max_length=200, verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    instagram = models.URLField(blank=True, verbose_name="Instagram")
    vk = models.URLField(blank=True, verbose_name="ВКонтакте")
    tiktok = models.URLField(blank=True, verbose_name="TikTok")
    youtube = models.URLField(blank=True, verbose_name="YouTube")

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"

    def __str__(self):
        return "Контактная информация магазина"

    def save(self, *args, **kwargs):
        # Ограничиваем количество записей одной
        if not self.pk and ContactInfo.objects.exists():
            return
        super().save(*args, **kwargs)

    def has_socials(self):
        return any([self.instagram, self.vk, self.tiktok, self.youtube])


class RentRules(models.Model):
    text = models.TextField(verbose_name="Правила аренды")

    class Meta:
        verbose_name = "Правила аренды"
        verbose_name_plural = "Правила аренды"

    def __str__(self):
        return "Правила аренды"

    def save(self, *args, **kwargs):
        # Ограничиваем количество записей одной
        if not self.pk and RentRules.objects.exists():
            return
        super().save(*args, **kwargs)


class TermsOfUse(models.Model):
    text = models.TextField(verbose_name="Условия использования")

    class Meta:
        verbose_name = "Условия использования"
        verbose_name_plural = "Условия использования"

    def __str__(self):
        return "Условия использования"

    def save(self, *args, **kwargs):
        if not self.pk and TermsOfUse.objects.exists():
            return
        super().save(*args, **kwargs)
