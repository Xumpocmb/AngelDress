from django.db import models
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage


class SliderImage(models.Model):
    desktop_image = models.ImageField(upload_to="slider/desktop/", verbose_name="Изображение для десктопа (16:9)")
    mobile_image = models.ImageField(
        upload_to="slider/mobile/",
        verbose_name="Изображение для мобильных (1:1)",
        blank=True,
        null=True,
        help_text="Если не указано, будет использоваться центральная часть десктопного изображения",
    )
    alt_text = models.CharField(max_length=100, blank=True, verbose_name="Альтернативный текст")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Изображение слайдера"
        verbose_name_plural = "Изображения слайдера"
        ordering = ["order"]

    def __str__(self):
        return f"Слайд {self.id}"

    def desktop_image_tag(self):
        if self.desktop_image:
            return mark_safe(f'<img src="{self.desktop_image.url}" width="150" />')
        return "Нет изображения"
    desktop_image_tag.short_description = "Предпросмотр (десктоп)"

    def mobile_image_tag(self):
        if self.mobile_image:
            return mark_safe(f'<img src="{self.mobile_image.url}" width="100" height="100" />')
        return "Нет изображения"
    mobile_image_tag.short_description = "Предпросмотр (мобильное)"

    def save(self, *args, **kwargs):
        # Удаляем старые изображения при обновлении
        if self.pk:
            old_instance = SliderImage.objects.get(pk=self.pk)
            if old_instance.desktop_image and old_instance.desktop_image != self.desktop_image:
                if default_storage.exists(old_instance.desktop_image.name):
                    default_storage.delete(old_instance.desktop_image.name)
            if old_instance.mobile_image and old_instance.mobile_image != self.mobile_image:
                if default_storage.exists(old_instance.mobile_image.name):
                    default_storage.delete(old_instance.mobile_image.name)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удаляем файлы изображений при удалении записи
        if self.desktop_image:
            if default_storage.exists(self.desktop_image.name):
                default_storage.delete(self.desktop_image.name)
        if self.mobile_image:
            if default_storage.exists(self.mobile_image.name):
                default_storage.delete(self.mobile_image.name)
        super().delete(*args, **kwargs)


class SocialTypes(models.Model):
    SOCIAL_TYPES = [
        ("phone", "Телефон"),
        ("address", "Адрес"),
        ("email", "Почта"),
        ("telegram", "Telegram"),
        ("instagram", "Instagram"),
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
        ("facebook", "Facebook"),
        ("x", "X (Twitter)"),
        ("linkedin", "LinkedIn"),
        ("snapchat", "Snapchat"),
        ("pinterest", "Pinterest"),
        ("reddit", "Reddit"),
        ("whatsapp", "WhatsApp"),
        ("discord", "Discord"),
        ("twitch", "Twitch"),
        ("vk", "VK"),
        ("viber", "Viber"),
    ]
    name = models.CharField(max_length=20, choices=SOCIAL_TYPES, verbose_name="Тип социальной сети")

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = "Тип социальной сети"
        verbose_name_plural = "Типы социальных сетей"


class ContactInfo(models.Model):
    type = models.ForeignKey(SocialTypes, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, null=True, verbose_name="Название")
    link = models.CharField(max_length=200, null=True, verbose_name="Данные контакта (ссылка, номер, и пр.)")
    is_active = models.BooleanField(default=True, verbose_name="Выводить на страницу?")

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"

    def __str__(self):
        return f"Контактная: {self.title}"


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


class Questions(models.Model):
    question_text = models.TextField(verbose_name="Вопрос", null=False, blank=False)
    answer_text = models.TextField(verbose_name="Ответ", null=False, blank=False)
    is_active = models.BooleanField(default=True, verbose_name="Выводить на страницу?")

    class Meta:
        db_table = "app_home_questions"
        verbose_name = "Частый вопрос"
        verbose_name_plural = "Частые вопросы"


class NewsTicker(models.Model):
    text = models.CharField(max_length=200, verbose_name="Текст бегущей строки")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Бегущая строка"
        verbose_name_plural = "Бегущие строки"

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.pk and NewsTicker.objects.exists():
            return
        super().save(*args, **kwargs)



class Counter(models.Model):
    name = models.CharField('Название счетчика', max_length=100, unique=True)
    value = models.CharField('Значение', max_length=20)
    label = models.CharField('Подпись', max_length=100)

    class Meta:
        verbose_name = 'Счетчик'
        verbose_name_plural = 'Счетчики'

    def __str__(self):
        return self.name