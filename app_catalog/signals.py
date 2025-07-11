from django.db.models import signals
from django.dispatch import receiver
from .models import Item, PriceOption

@receiver(signals.post_save, sender=PriceOption)
def update_item_min_price_on_create(sender, instance, **kwargs):
    instance.item.update_min_price()


@receiver(signals.post_delete, sender=PriceOption)
def update_item_min_price_on_delete(sender, instance, **kwargs):
    instance.item.update_min_price()
