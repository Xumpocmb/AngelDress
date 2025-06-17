from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
import json

from app_catalog.models import Dress


def wishlist_view(request):
    return render(request, 'app_wishlist/wishlist.html')


def toggle_wishlist(request, dress_id):
    if request.method == 'POST':
        wishlist = request.session.get('wishlist', [])
        dress = get_object_or_404(Dress, pk=dress_id)

        if dress_id in wishlist:
            wishlist.remove(dress_id)
            status = 'removed'
            if dress.favorites_count > 0:
                dress.favorites_count -= 1
        else:
            wishlist.append(dress_id)
            status = 'added'
            dress.favorites_count += 1

        request.session['wishlist'] = wishlist
        request.session.modified = True  # Важно при изменении сессии

        # Обновляем рейтинг популярности
        dress.update_popularity()

        return JsonResponse({'status': status, 'count': len(wishlist)})

    return HttpResponse(status=400)


def get_wishlist_count(request):
    wishlist = request.session.get('wishlist', [])
    return HttpResponse(
        json.dumps({'count': len(wishlist)}),
        content_type='application/json'
    )
