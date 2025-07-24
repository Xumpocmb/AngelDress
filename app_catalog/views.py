from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from app_catalog.models import Item, ItemCategory, Accessory, AccessoryCategory, ItemCharacteristic, Color, Size, \
    Material, Brand
from app_home.models import RentRules


def item_catalog_view(request):
    # Получаем параметры фильтрации из GET-запроса
    category_slug = request.GET.get("category")
    search_query = request.GET.get("search", "")
    sort = request.GET.get("sort", "newest")
    page = request.GET.get("page", "1")

    # Получаем параметры фильтрации из GET
    color_ids = request.GET.getlist("color")
    size_ids = request.GET.getlist("size")
    material_ids = request.GET.getlist("material")
    brand_ids = request.GET.getlist("brand")
    price_ranges = request.GET.getlist("price_range")
    lengths = request.GET.getlist("length")
    fits = request.GET.getlist("fit")
    sleeves = request.GET.getlist("sleeve")
    trains = request.GET.getlist("train")

    # Базовый запрос
    items = Item.objects.filter(is_active=True).prefetch_related(
        "categories", "colors", "available_sizes", "materials"
    ).select_related("brand", "characteristics")

    # Фильтрация по категории
    if category_slug:
        items = items.filter(categories__slug=category_slug)

    # Поиск по тексту
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(details__icontains=search_query) |
            Q(colors__name__icontains=search_query) |
            Q(available_sizes__name__icontains=search_query) |
            Q(materials__name__icontains=search_query)
        ).distinct()

    # Фильтрация по цветам
    if color_ids:
        items = items.filter(colors__id__in=color_ids).distinct()

    # Фильтрация по размерам
    if size_ids:
        items = items.filter(available_sizes__id__in=size_ids).distinct()

    # Фильтрация по материалам
    if material_ids:
        items = items.filter(materials__id__in=material_ids).distinct()

    # Фильтрация по брендам
    if brand_ids:
        items = items.filter(brand__id__in=brand_ids).distinct()

    # Фильтрация по характеристикам
    characteristics_filters = {}
    if price_ranges:
        characteristics_filters['price_range__in'] = price_ranges
    if lengths:
        characteristics_filters['length__in'] = lengths
    if fits:
        characteristics_filters['fit__in'] = fits
    if sleeves:
        characteristics_filters['sleeve__in'] = sleeves
    if trains:
        characteristics_filters['train__in'] = trains

    if characteristics_filters:
        items = items.filter(characteristics__in=ItemCharacteristic.objects.filter(**characteristics_filters)).distinct()

    # Сортировка
    if sort == "price-low":
        items = items.order_by("min_price")
    elif sort == "price-high":
        items = items.order_by("-min_price")
    elif sort == "popular":
        items = items.order_by("-popularity_score", "-views_count", "-favorites_count")
    else:  # default to newest
        items = items.order_by("-created_at")

    # Пагинация
    paginator = Paginator(items.distinct(), 9)
    page_obj = paginator.get_page(page)

    # Получаем все доступные варианты для фильтров
    colors = Color.objects.annotate(num_items=Count('item')).filter(num_items__gt=0).order_by('name')
    sizes = Size.objects.annotate(num_items=Count('item')).filter(num_items__gt=0).order_by('order')
    materials = Material.objects.annotate(num_items=Count('item')).filter(num_items__gt=0).order_by('name')
    brands = Brand.objects.annotate(num_items=Count('item')).filter(num_items__gt=0).order_by('name')

    # Получаем уникальные значения для характеристик
    price_range_choices = dict(ItemCharacteristic.PRICE_RANGE_CHOICES)
    length_choices = dict(ItemCharacteristic.LENGTH_CHOICES)
    fit_choices = dict(ItemCharacteristic.FIT_CHOICES)
    sleeve_choices = dict(ItemCharacteristic.SLEEVE_CHOICES)
    train_choices = dict(ItemCharacteristic.TRAIN_CHOICES)

    context = {
        "page_obj": page_obj,
        "categories": ItemCategory.objects.filter(is_active=True),
        "current_category": category_slug,
        "current_sort": sort,
        "search_query": search_query,
        "model_type": "dress",
        # Параметры фильтрации
        "colors": colors,
        "sizes": sizes,
        "materials": materials,
        "brands": brands,
        "price_range_choices": price_range_choices,
        "length_choices": length_choices,
        "fit_choices": fit_choices,
        "sleeve_choices": sleeve_choices,
        "train_choices": train_choices,
        # Текущие выбранные фильтры
        "selected_colors": color_ids,
        "selected_sizes": size_ids,
        "selected_materials": material_ids,
        "selected_brands": brand_ids,
        "selected_price_ranges": price_ranges,
        "selected_lengths": lengths,
        "selected_fits": fits,
        "selected_sleeves": sleeves,
        "selected_trains": trains,
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
        "model_type": "dress",
        "meta_description": f"{dress.name}: прокат платьев в Москве, вечерние, свадебные, выпускные. Забронируйте прямо сейчас!",
    }
    return render(request, "app_catalog/product.html", context)


def accessory_catalog_view(request):
    category_slug = request.GET.get("category", "")
    search_query = request.GET.get("search", "")
    sort = request.GET.get("sort", "newest")
    page = request.GET.get("page", "1")

    request.session['catalog_params'] = {
        'category': category_slug,
        'search': search_query,
        'sort': sort,
        'page': page,
        'model_type': 'accessory'
    }

    accessories = Accessory.objects.filter(is_active=True).prefetch_related("categories")

    if category_slug:
        accessories = accessories.filter(categories__slug=category_slug)

    if search_query:
        accessories = accessories.filter(
            Q(color__icontains=search_query.strip()) |
            Q(details__icontains=search_query.strip())
        )

    if sort == "price-low":
        accessories = accessories.order_by("min_price")
    elif sort == "price-high":
        accessories = accessories.order_by("-min_price")
    elif sort == "popular":
        accessories = accessories.order_by("-popularity_score", "-views_count", "-favorites_count")
    else:
        accessories = accessories.order_by("-created_at")

    paginator = Paginator(accessories, 9)
    page_obj = paginator.get_page(page)

    context = {
        "page_obj": page_obj,
        "categories": AccessoryCategory.objects.filter(is_active=True),
        "current_category": category_slug,
        "current_sort": sort,
        "search_query": search_query,
        "model_type": "accessory",
        "title": "Каталог аксессуаров",
        "meta_description": "Прокат аксессуаров в Москве: украшения, сумки и многое другое. Забронируйте прямо сейчас!",
    }
    return render(request, "app_catalog/catalog.html", context)


def accessory_detail_view(request, accessory_id):
    accessory = get_object_or_404(Accessory, pk=accessory_id, is_active=True)
    accessory.views_count += 1
    accessory.save(update_fields=["views_count"])
    accessory.update_popularity()

    images = list(accessory.images.all())
    videos = list(accessory.videos.all())
    media_files = sorted(images + videos, key=lambda x: x.order)

    catalog_params = request.session.get('catalog_params', {})

    rent_rules = RentRules.objects.first()
    rent_rules_text = rent_rules.text if rent_rules else "Правила аренды не определены"

    context = {
        "product": accessory,
        "images": images,
        "rent_rules_text": rent_rules_text,
        "media_files": media_files,
        "catalog_params": catalog_params,
        "model_type": "accessory",
        "meta_description": f"{accessory.name}: прокат аксессуаров в Москве. Забронируйте прямо сейчас!",
    }
    return render(request, "app_catalog/product.html", context)