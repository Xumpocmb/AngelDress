from django.shortcuts import render
from django.shortcuts import HttpResponse, get_object_or_404
import json

from app_catalog.models import Dress


def wishlist_view(request):
    return render(request, 'app_wishlist/wishlist.html')


def toggle_favorite(request, dress_id):
    if request.method == 'POST':
        dress = get_object_or_404(Dress, pk=dress_id)
        wishlist = request.session.get('wishlist', [])

        if dress_id in wishlist:
            wishlist.remove(dress_id)
            status = 'removed'
        else:
            wishlist.append(dress_id)
            status = 'added'

        request.session['wishlist'] = wishlist
        return HttpResponse(
            json.dumps({'status': status, 'count': len(wishlist)}),
            content_type='application/json'
        )
    return HttpResponse(status=400)


def get_wishlist_count(request):
    wishlist = request.session.get('wishlist', [])
    return HttpResponse(
        json.dumps({'count': len(wishlist)}),
        content_type='application/json'
    )
