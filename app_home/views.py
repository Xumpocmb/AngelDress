from calendar import c
import random

from django.shortcuts import render

from app_blog.models import Post
from app_catalog.models import Item, ItemCategory
from app_home.models import RentRules, SliderImage, ContactInfo, TermsOfUse


def index_view(request):
    slider_images = SliderImage.objects.all().order_by("order")
    accessory_category = ItemCategory.objects.get(slug="aksessuary")

    # 6 случайных платьев
    random_dresses = Item.objects.filter(is_active=True).exclude(categories=accessory_category).prefetch_related("images").order_by("?")[:6]

    # 3 последних блога
    latest_posts = Post.objects.all().order_by("-created_at")[:3]

    # 2 случайных аксессуара
    random_accessories = Item.objects.filter(is_active=True, categories=accessory_category).prefetch_related("images").order_by("?")[:2]

    context = {
        "slider_images": slider_images,
        "random_dresses": random_dresses,
        "latest_posts": latest_posts,
        "random_accessories": random_accessories,
    }
    return render(request, "app_home/index.html", context=context)


def contact_view(request):
    return render(request, "app_home/contacts.html")


def about_view(request):
    return render(request, "app_home/about.html")


def user_agreement_view(request):
    rent_rules = RentRules.objects.first()
    terms_of_use = TermsOfUse.objects.first()

    if terms_of_use:
        terms_of_use_text = terms_of_use.text
    else:
        terms_of_use_text = "Условия использования не определены"

    if rent_rules:
        rent_rules_text = rent_rules.text
    else:
        rent_rules_text = "Правила аренды не определены"

    context = {
        "rent_rules_text": rent_rules_text,
        "terms_of_use_text": terms_of_use_text,
    }
    return render(request, "app_home/user_agreement.html", context=context)
