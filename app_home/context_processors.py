from app_home.models import ContactInfo


def contact_info(request):
    try:
        contacts = ContactInfo.objects.first()
        return {'contact_info': contacts or None}
    except Exception:
        return {'contact_info': None}
