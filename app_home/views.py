from django.shortcuts import render

from app_catalog.models import Dress, DressCategory
from app_home.models import RentRules, SliderImage, TermsOfUse


def index_view(request):
    slider_images = SliderImage.objects.all().order_by("order")

    random_dresses = Dress.objects.prefetch_related("images").order_by("?")[:6]

    main_page_categories = DressCategory.objects.filter(show_on_main_page=True)[:4]

    context = {
        "slider_images": slider_images,
        "random_dresses": random_dresses,
        "main_page_categories": main_page_categories,
    }
    return render(request, "app_home/index.html", context=context)


def grouper(iterable, n):
    """Группирует элементы списка по n штук"""
    return [iterable[i : i + n] for i in range(0, len(iterable), n)]


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
