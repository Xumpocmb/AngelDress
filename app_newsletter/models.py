from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"


class Newsletter(models.Model):
    subject = models.CharField("Тема", max_length=255)
    content = models.TextField("Содержание")
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    def send(self):
        from django.core.mail import EmailMultiAlternatives

        subscribers = Subscriber.objects.values_list('email', flat=True)
        if not subscribers:
            return

        # Рендерим HTML и текстовую версию письма
        html_content = render_to_string('emails/newsletter.html', {'content': self.content})
        text_content = strip_tags(html_content)

        # Настройка письма
        subject = self.subject
        from_email = settings.DEFAULT_FROM_EMAIL

        for email in subscribers:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)

        self.sent = True
        self.save()

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
