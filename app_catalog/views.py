from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from app_catalog.models import Item, ItemCategory
from app_home.models import RentRules


def item_catalog_view(request):
    category_slug = request.GET.get("category")
    search_query = request.GET.get("search", "")
    dresses = Item.objects.filter(is_active=True).prefetch_related("categories")
    sort = request.GET.get("sort", "newest")
    page = request.GET.get("page", "1")

    request.session['catalog_params'] = {
        'category': category_slug,
        'search': search_query,
        'sort': sort,
        'page': page
    }

    if category_slug:
        dresses = dresses.filter(categories__slug=category_slug)

    if search_query:
        dresses = dresses.filter(
            Q(color__icontains=search_query.strip()) |
            Q(available_sizes__icontains=search_query.strip())
        )

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
        "search_query": search_query,
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

    catalog_params = request.session.get('catalog_params', {})

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
        'catalog_params': catalog_params,
        "meta_description": f"{dress.name}: прокат платьев в Москве, вечерние, свадебные, выпускные. Забронируйте прямо сейчас!",
    }
    return render(request, "app_catalog/product.html", context)
