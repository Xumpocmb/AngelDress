import re
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from app_catalog.models import Dress, DressCategory
from app_home.models import RentRules


def dress_catalog_view(request):
    category_slug = request.GET.get("category")  # Получаем выбранную категорию из URL

    # Получаем все платья с фильтрацией по категории
    dresses = Dress.objects.all()
    if category_slug:
        dresses = dresses.filter(category__slug=category_slug)

    sort = request.GET.get("sort", "newest")
    if sort == "price-low":
        dresses = dresses.order_by("price_min")
    elif sort == "price-high":
        dresses = dresses.order_by("-price_min")
    elif sort == "popular":
        dresses = dresses.order_by("-popularity_score")
    else:
        dresses = dresses.order_by("-created_at")

    paginator = Paginator(dresses, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "categories": DressCategory.objects.all(),
        "current_category": category_slug,
        "current_sort": sort,
    }
    return render(request, "app_catalog/catalog.html", context)


def dress_detail_view(request, dress_id):
    dress = get_object_or_404(Dress, pk=dress_id)

    dress.views_count += 1
    dress.save(update_fields=["views_count"])

    dress.update_popularity()

    images = dress.images.all().order_by("order")
    main_image = images.first() if images.exists() else None

    rent_rules = RentRules.objects.first()
    if rent_rules:
        rent_rules_text = rent_rules.text
    else:
        rent_rules_text = "Правила аренды не определены"
    

    context = {
        "product": dress,
        "main_image": main_image,
        "images": images,
        "rent_rules_text": rent_rules_text,
    }
    return render(request, "app_catalog/product.html", context)
