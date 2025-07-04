import json
import logging

import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.template.loader import render_to_string

from app_newsletter.models import Subscriber
from .forms import ClientCallBackForm

logger = logging.getLogger(__name__)
from django.db import transaction

from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit


@require_http_methods(["POST"])
@ratelimit(key='ip', rate='1/m', block=True)
def ajax_callback_view(request):
    logger.info("ajax_callback_view вызвана")

    # Проверка Content-Type
    if request.content_type != 'application/json':
        logger.warning(f"Неверный Content-Type: {request.content_type}")
        return JsonResponse(
            {"success": False, "errors": {"__all__": ["Неверный Content-Type, ожидается application/json"]}},
            status=415
        )

    # Проверка размера тела запроса
    max_body_size = 1024  # 1KB
    body_length = len(request.body)
    logger.debug(f"Размер тела запроса: {body_length} байт")
    if body_length > max_body_size:
        logger.warning(f"Слишком большой размер запроса: {body_length} байт")
        return JsonResponse(
            {"success": False, "errors": {"__all__": ["Слишком большой размер запроса"]}},
            status=413
        )

    # Парсинг JSON
    try:
        data = json.loads(request.body.decode('utf-8'))
        logger.debug(f"Полученные данные: {data}")

        # Проверка длины полей
        max_field_length = 100
        for field in ['name', 'phone', 'email']:
            if field in data and len(data[field]) > max_field_length:
                logger.warning(f"Поле '{field}' слишком длинное: {len(data[field])} символов")
                return JsonResponse(
                    {"success": False, "errors": {field: ["Слишком длинное значение"]}},
                    status=400
                )

        # Валидация email
        if 'email' in data and '@' not in data['email']:
            logger.warning(f"Некорректный email: {data['email']}")
            return JsonResponse(
                {"success": False, "errors": {"email": ["Некорректный email"]}},
                status=400
            )

    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.warning(f"Invalid request data from {request.META.get('REMOTE_ADDR')}: {str(e)}", exc_info=True)
        return JsonResponse(
            {"success": False, "errors": {"__all__": ["Некорректный формат данных"]}},
            status=400,
        )

    # Создание формы
    form = ClientCallBackForm(data)
    logger.info("Форма создана")

    if form.is_valid():
        logger.info("Форма прошла валидацию")
        try:
            call_request = form.save(commit=False)

            # Очистка и сохранение полей
            call_request.name = clean_string(form.cleaned_data.get('name', ''))
            call_request.phone = clean_phone(form.cleaned_data.get('phone', ''))
            call_request.email = form.cleaned_data.get('email', '').lower().strip()
            call_request.save()
            logger.info(f"Запрос обратного звонка сохранён: ID={call_request.id}")

            # Работа с подписчиком
            try:
                with transaction.atomic():
                    subscriber, created = Subscriber.objects.get_or_create(
                        email=call_request.email,
                        defaults={'is_active': True}
                    )
                    logger.info(f"Подписчик {'создан' if created else 'уже существует'}: {call_request.email}")
            except Exception as e:
                logger.error(f"Ошибка при работе с подписчиком: {str(e)}", exc_info=True)

            # Отправка email
            try:
                context = {
                    "user_name": call_request.name,
                    "phone": call_request.phone,
                }

                plain_message = render_to_string("emails/client_call_back.txt", context)
                html_message = render_to_string("emails/client_call_back.html", context)

                email = EmailMultiAlternatives(
                    subject="Подтверждение запроса на обратный звонок от Angel Dress",
                    body=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[call_request.email],
                    headers={'X-Entity-Ref-ID': str(call_request.id)},
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)
                logger.info(f"Email отправлен на {call_request.email}")
            except Exception as e:
                logger.error(f"Не удалось отправить email: {str(e)}", exc_info=True)

            # Уведомление в Telegram
            try:
                telegram_token = settings.TELEGRAM_BOT_TOKEN
                telegram_chat_id = settings.TELEGRAM_CHAT_ID

                message_text = (
                    f"🔔 Новая заявка на обратный звонок!\n\n"
                    f"👤 Имя: {call_request.name}\n"
                    f"📞 Телефон: {call_request.phone}\n"
                    f"📧 Email: {call_request.email}\n"
                    f"🔗 ID: {call_request.id}"
                )

                if not str(telegram_chat_id).startswith('-100'):
                    raise ValueError("Некорректный формат chat_id для Telegram")

                send_url = f"https://api.telegram.org/bot {telegram_token}/sendMessage"

                with requests.Session() as session:
                    session.timeout = 5
                    response = session.post(
                        send_url,
                        json={
                            "chat_id": telegram_chat_id,
                            "text": message_text,
                            "disable_web_page_preview": True,
                        },
                        timeout=5
                    )
                    response.raise_for_status()

                logger.info(f"Telegram-сообщение успешно отправлено: ID={call_request.id}")
            except Exception as e:
                logger.error(f"Не удалось отправить уведомление в Telegram: {str(e)}", exc_info=True)

            return JsonResponse({"success": True}, headers={'X-Frame-Options': 'DENY'})

        except Exception as e:
            logger.critical(f"Критическая ошибка в обработке запроса: {str(e)}", exc_info=True)
            return JsonResponse(
                {"success": False, "errors": {"__all__": ["Внутренняя ошибка сервера"]}},
                status=500,
                headers={'X-Content-Type-Options': 'nosniff'}
            )
    else:
        logger.warning(f"Форма не прошла валидацию: {form.errors}")
        return JsonResponse(
            {"success": False, "errors": form.errors},
            status=400,
            headers={'Cache-Control': 'no-store'}
        )


# Вспомогательные функции безопасности
def clean_string(value):
    """Очистка строки от потенциально опасных символов"""
    import re
    return re.sub(r'[^\w\s\-@\.]', '', value.strip())


def clean_phone(phone):
    """Нормализация номера телефона"""
    import re
    return re.sub(r'[^\d+]', '', phone.strip())

