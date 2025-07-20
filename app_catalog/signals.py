from django.db.models import signals
from django.dispatch import receiver
from .models import Item, PriceOption

@receiver(signals.post_save, sender=PriceOption)
def update_item_min_price_on_create(sender, instance, **kwargs):
    if instance.item:
        instance.item.update_min_price()
    elif instance.accessory:
        instance.accessory.update_min_price()
