import json

import requests
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit

from app_catalog.models import Accessory
from app_newsletter.models import Subscriber
from .forms import RentalRequestForm
from .models import Item


@require_http_methods(["POST"])
# @ratelimit(key='ip', rate='1/m', block=True)
def create_rental_request(request):
    if not request.content_type.startswith('multipart/form-data'):
        return JsonResponse(
            {"success": False, "error": "Неверный Content-Type"},
            status=415
        )

    if len(request.POST) > 20:
        raise SuspiciousOperation("Слишком много полей в запросе")

    print("POST data:", request.POST)
    print("item_ids:", request.POST.get("item_ids"))

    form = RentalRequestForm(request.POST)

    if form.is_valid():
        try:
            try:
                item_ids = json.loads(request.POST.get("item_ids", "[]"))
                item_ids = [int(did) for did in item_ids if str(did).isdigit() and int(did) > 0]
            except (json.JSONDecodeError, ValueError, TypeError) as e:
                return JsonResponse(
                    {"success": False, "error": "Неверный формат списка товаров"},
                    status=400
                )
            if not isinstance(item_ids, list):
                raise ValueError("Неверный формат item_ids")

            if len(item_ids) > 10:
                return JsonResponse(
                    {"success": False, "error": "Можно выбрать не более 10 товаров"},
                    status=400
                )

            if not item_ids:
                return JsonResponse(
                    {"success": False, "error": "Не выбрано ни одного товара"},
                    status=400
                )

            # Fetch Items and Accessories
            items = Item.objects.filter(id__in=item_ids).distinct()
            accessories = Accessory.objects.filter(id__in=item_ids).distinct()
            all_items = list(items) + list(accessories)

            if len(all_items) > 10:
                all_items = all_items[:10]

            if not all_items:
                return JsonResponse(
                    {"success": False, "error": "Не найдено ни одного товара"},
                    status=400
                )

            with transaction.atomic():
                rental_request = form.save(commit=False)
                rental_request.name = clean_string(form.cleaned_data['name'])
                rental_request.phone = clean_phone(form.cleaned_data['phone'])
                rental_request.email = form.cleaned_data['email'].lower().strip()
                rental_request.save()

                # Set Items and Accessories
                rental_request.items.set([item for item in all_items if isinstance(item, Item)])
                rental_request.accessories.set([item for item in all_items if isinstance(item, Accessory)])

                try:
                    Subscriber.objects.get_or_create(
                        email=rental_request.email,
                        defaults={'is_active': True}
                    )
                except Exception as e:
                    pass

            try:
                context = {
                    "user_name": rental_request.name,
                    "request_id": rental_request.id,
                    "items": all_items,  # Combined list for email
                    "phone": rental_request.phone,
                }

                text_body = render_to_string("emails/rental_confirmation.txt", context)
                html_body = render_to_string("emails/rental_confirmation.html", context)

                email = EmailMultiAlternatives(
                    subject="Подтверждение заявки на бронирование Angel Dress",
                    body=text_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[rental_request.email],
                    headers={
                        'X-Entity-Ref-ID': str(rental_request.id),
                        'X-Content-Type-Options': 'nosniff'
                    },
                )
                email.attach_alternative(html_body, "text/html")
                email.send(fail_silently=False)

            except Exception as e:
                print(f"Email sending failed: {str(e)}")

            try:
                telegram_token = settings.TELEGRAM_BOT_TOKEN
                telegram_chat_id = settings.TELEGRAM_CHAT_ID

                items_list = "\n".join([f"- {item.name} (ID: {item.id})" for item in all_items])

                message_text = (
                    f"🔔 Новая заявка на бронирование примерки!\n\n"
                    f"👤 Имя: {rental_request.name}\n"
                    f"📞 Телефон: {rental_request.phone}\n"
                    f"📧 Email: {rental_request.email}\n"
                    f"🛍️ Выбранные товары:\n{items_list}\n"
                    f"🔗 ID заявки: {rental_request.id}"
                )

                send_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

                with requests.Session() as session:
                    session.timeout = 5
                    response = session.post(
                        send_url,
                        json={
                            "chat_id": telegram_chat_id,
                            "text": message_text,
                        },
                        timeout=5
                    )
                    response.raise_for_status()

            except Exception as e:
                print(f"Telegram notification failed: {str(e)}")

            return JsonResponse(
                {"success": True},
                headers={
                    'X-Frame-Options': 'DENY',
                    'Content-Security-Policy': "default-src 'self'"
                }
            )

        except Exception as e:
            print(f"Rental request error: {str(e)}")
            return JsonResponse(
                {"success": False, "error": "Внутренняя ошибка сервера"},
                status=500,
                headers={'X-Content-Type-Options': 'nosniff'}
            )
    else:
        print(f"Form errors: {form.errors}")
        return JsonResponse(
            {"success": False, "errors": form.errors},
            status=400,
            headers={'Cache-Control': 'no-store'}
        )



def clean_string(value):
    """Очистка строки от опасных символов"""
    import re
    return re.sub(r'[^\w\s\-@\.а-яА-Я]', '', str(value).strip())


def clean_phone(phone):
    """Нормализация телефона"""
    import re
    return re.sub(r'[^\d+]', '', str(phone).strip())


