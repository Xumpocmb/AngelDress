import json
import re

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from app_newsletter.models import Subscriber
from .forms import RentalRequestForm
from .models import Dress

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import RentalRequestForm
from .models import Dress
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


# @require_POST
def create_rental_request(request):
    print("create_rental_request")
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Метод должен быть POST'})
    
    form = RentalRequestForm(request.POST)
    if form.is_valid():
        rental_request = form.save(commit=False)
        dress_ids = json.loads(request.POST.get('dress_ids', '[]'))
        dresses = Dress.objects.filter(id__in=dress_ids)
        if not dresses.exists():
            return JsonResponse({'success': False, 'error': 'Не выбрано ни одного платья'})

        rental_request.save()
        rental_request.dresses.set(dresses)

        try:
            email = rental_request.email
            subscriber = Subscriber.objects.create(email=email)
        except Exception as e:
            pass

        try:
            context = {
                'user_name': rental_request.name,
                'request_id': rental_request.id,
                'dresses': dresses,
                'phone': rental_request.phone,
            }
            # Рендерим текстовую и HTML версии из файлов-шаблонов
            text_body = render_to_string('emails/rental_confirmation.txt', context)
            html_body = render_to_string('emails/rental_confirmation.html', context)

            email = EmailMultiAlternatives(
                subject='Подтверждение заявки на бронирование Angel Dress',
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[rental_request.email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)

        except Exception as e:
            print("Ошибка при отправке email:")
            print("Ошибка:", str(e))
            return JsonResponse({
                'success': False,
                'errors': {
                    'email': 'Не удалось отправить письмо с подтверждением. Пожалуйста, свяжитесь с нами напрямую.'
                }
            }, status=500)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})
