import json

from django.http import HttpResponse

from app_catalog.models import ItemCategory
from app_home.models import ContactInfo


def contact_info(request):
    try:
        contacts = ContactInfo.objects.all()
        return {'contact_info': contacts or None}
    except Exception:
        return {'contact_info': None}


def get_wishlist_count(request):
    wishlist = request.session.get("wishlist", [])
    return {"wishlist_count": len(wishlist)}


def get_main_page_categories(request):
    main_page_categories = ItemCategory.objects.filter(show_on_main_page=True, is_active=True)[:4]
    return {"main_page_categories": main_page_categories}