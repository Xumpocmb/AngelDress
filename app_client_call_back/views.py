import json

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from app_newsletter.models import Subscriber
from .forms import ClientCallBackForm


@require_POST
def ajax_callback_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'errors': {'__all__': ['Некорректный формат данных']}}, status=400)

    form = ClientCallBackForm(data)

    if form.is_valid():
        call_request = form.save()

        try:
            email = call_request.email
            subscriber = Subscriber.objects.create(email=email)
        except Exception as e:
            pass

        try:
            context = {
                'user_name': call_request.name,
                'phone': call_request.phone,
            }

            plain_message = render_to_string('emails/client_call_back.txt', context)
            html_message = render_to_string('emails/client_call_back.html', context)

            email = EmailMultiAlternatives(
                subject='Подтверждение запроса на обратный звонок от Angel Dress',
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[call_request.email],
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)

        except Exception as e:
            return JsonResponse({'success': False, 'errors': {'email': 'Не удалось отправить письмо с подтверждением. Пожалуйста, свяжитесь с нами напрямую.'}}, status=500)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
