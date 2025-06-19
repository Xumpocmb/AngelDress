import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import ClientCallBackForm


@require_POST
def ajax_callback_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'errors': {'__all__': ['Некорректный формат данных']}}, status=400)

    form = ClientCallBackForm(data)

    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
