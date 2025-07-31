from django.utils import timezone

from app_catalog.models import ItemCategory
from app_home.models import ContactInfo, Counter, SliderImage
from app_promotion.models import Promotion


def contact_info(request):
    try:
        contacts = ContactInfo.objects.all()
        header_contacts = ContactInfo.objects.filter(
            type__name__in=["telegram", "instagram", "phone"], is_active=True
        )
        return {
            "contact_info": contacts or None,
            "header_contacts": header_contacts or None,
        }
    except Exception:
        return {"contact_info": None, "header_contacts": None}


def get_wishlist_count(request):
    wishlist = request.session.get("wishlist", [])
    return {"wishlist_count": len(wishlist)}


def get_main_page_categories(request):
    main_page_categories = ItemCategory.objects.filter(
        show_on_main_page=True, is_active=True
    )[:4]
    return {"main_page_categories": main_page_categories}


def counters(request):
    def get_counter_value(name, default=0):
        try:
            return Counter.objects.get(name=name).value
        except Counter.DoesNotExist:
            return default

    return {
        'counters': {
            'dresses': get_counter_value('Платья выбрано'),
            'clients': get_counter_value('Довольные клиенты'),
            'new_items': get_counter_value('Новые поступления'),
        }
    }

def active_promotions(request):
    context = {}

    slider_images = SliderImage.objects.all().order_by("order")

    promotions = Promotion.objects.filter(
        is_active=True,
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date()
    ).order_by('order')

    if promotions.exists():
        context['slider_content'] = {'type': 'promotions', 'items': promotions}
    elif slider_images.exists():
        context['slider_content'] = {'type': 'images', 'items': slider_images}

    return context