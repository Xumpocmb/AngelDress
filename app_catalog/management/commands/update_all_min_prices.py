from django.core.management.base import BaseCommand
from app_catalog.models import Item


class Command(BaseCommand):
    help = "Обновляет min_price для всех товаров"

    def handle(self, *args, **options):
        for item in Item.objects.all():
            item.update_min_price()
            self.stdout.write(f"Обновлено: {item.name} — {item.min_price}")
