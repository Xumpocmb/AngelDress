import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_catalog.models import Dress


def wishlist_view(request) -> HttpResponse:
    wishlist = request.session.get("wishlist", [])
    valid_wishlist = []

    if wishlist:
        # Проверяем, существуют ли такие Dress в БД
        wishlist_ids = [int(dress_id) for dress_id in wishlist]
        existing_dresses = Dress.objects.filter(id__in=wishlist_ids).values_list(
            "id", flat=True
        )

        valid_wishlist = [
            str(dress_id) for dress_id in wishlist_ids if dress_id in existing_dresses
        ]

        request.session["wishlist"] = valid_wishlist
        request.session.modified = True

        dresses = Dress.objects.filter(id__in=valid_wishlist).order_by("-created_at")

        paginator = Paginator(dresses, 9)
        page_number = request.GET.get("page")

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    else:
        paginator = Paginator(Dress.objects.none(), 9)
        page_obj = paginator.page(1)

    context = {
        "page_obj": page_obj,
        "wishlist": valid_wishlist,
    }
    return render(request, "app_wishlist/wishlist.html", context=context)


def toggle_wishlist(request, dress_id):
    if request.method == "POST":
        wishlist = request.session.get("wishlist", [])
        dress = get_object_or_404(Dress, pk=dress_id)

        if dress_id in wishlist:
            wishlist.remove(dress_id)
            status = "removed"
            if dress.favorites_count > 0:
                dress.favorites_count -= 1
        else:
            wishlist.append(dress_id)
            status = "added"
            dress.favorites_count += 1

        request.session["wishlist"] = wishlist
        request.session.modified = True

        dress.update_popularity()

        return JsonResponse({"status": status, "count": len(wishlist)})

    return HttpResponse(status=400)


def wishlist_count(request):
    wishlist = request.session.get("wishlist", [])
    return JsonResponse({"count": len(wishlist)})
