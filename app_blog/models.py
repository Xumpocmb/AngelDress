import os

from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class SocialTypes(models.Model):
    SOCIAL_TYPES = [
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
    ]
    name = models.CharField(
        max_length=20, choices=SOCIAL_TYPES, verbose_name="Тип социальной сети"
    )

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = "Тип социальной сети"
        verbose_name_plural = "Типы социальных сетей"


class AuthorSocial(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    type = models.ForeignKey(SocialTypes, on_delete=models.SET_NULL, null=True)
    link = models.URLField("Ссылка", blank=True, null=True)

    def __str__(self):
        return f"{self.author.name} - {self.type.get_name_display()}"

    class Meta:
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Post(models.Model):
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, related_name="posts")
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="blog_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(Post, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def get_absolute_url(self):
        return reverse("app_blog:post", args=[self.id])
