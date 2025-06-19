from django.apps import AppConfig


class AppBookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_book'

    verbose_name = 'Заявки на примерку'
