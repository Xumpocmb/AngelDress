import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import RentalRequestForm
from .models import Dress


@require_POST
def create_rental_request(request):
    form = RentalRequestForm(request.POST)

    if form.is_valid():
        # Получаем данные из формы
        rental_request = form.save(commit=False)

        # Получаем список ID платьев из POST-запроса
        dress_ids = json.loads(request.POST.get('dress_ids', '[]'))
        dresses = Dress.objects.filter(id__in=dress_ids)

        if not dresses.exists():
            return JsonResponse({'success': False, 'error': 'Не выбрано ни одного платья'})

        # Сохраняем заявку
        rental_request.save()

        # Добавляем платья в заявку
        rental_request.dresses.set(dresses)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})
