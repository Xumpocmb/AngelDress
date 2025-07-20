from django import template
from django.urls import reverse
from app_catalog.models import Item, Accessory

register = template.Library()

@register.simple_tag
def get_item_url(obj):
    if isinstance(obj, Item):
        return reverse("app_catalog:item_detail", args=[obj.id])
    elif isinstance(obj, Accessory):
        return reverse("app_catalog:accessory_detail", args=[obj.id])
    return "#"