from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from app_catalog.models import Item, ItemCategory
from app_home.models import RentRules


def item_catalog_view(request):
    category_slug = request.GET.get("category")
    dresses = Item.objects.filter(is_active=True).prefetch_related("categories")

    if category_slug:
        dresses = dresses.filter(categories__slug=category_slug)

    # Сортировка
    sort = request.GET.get("sort", "newest")

    if sort == "price-low":
        dresses = dresses.order_by("min_price")
    elif sort == "price-high":
        dresses = dresses.order_by("-min_price")
    elif sort == "popular":
        dresses = dresses.order_by(
            "-popularity_score", "-views_count", "-favorites_count"
        )
    else:
        dresses = dresses.order_by("-created_at")

    paginator = Paginator(dresses, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "categories": ItemCategory.objects.filter(is_active=True),
        "current_category": category_slug,
        "current_sort": sort,
        "meta_description": "Прокат платьев в Москве, вечерние, свадебные, выпускные. Забронируйте прямо сейчас!",
    }
    return render(request, "app_catalog/catalog.html", context)


def item_detail_view(request, dress_id):
    dress = get_object_or_404(Item, pk=dress_id)

    dress.views_count += 1
    dress.save(update_fields=["views_count"])

    dress.update_popularity()

    images = list(dress.images.all())
    videos = list(dress.videos.all())
    media_files = sorted(images + videos, key=lambda x: x.order)

    rent_rules = RentRules.objects.first()
    if rent_rules:
        rent_rules_text = rent_rules.text
    else:
        rent_rules_text = "Правила аренды не определены"

    context = {
        "product": dress,
        "images": images,
        "rent_rules_text": rent_rules_text,
        "media_files": media_files,
        "meta_description": f"{dress.name}: прокат платьев в Москве, вечерние, свадебные, выпускные. Забронируйте прямо сейчас!",
    }
    return render(request, "app_catalog/product.html", context)
