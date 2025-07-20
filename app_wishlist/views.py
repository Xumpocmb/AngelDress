import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_catalog.models import Item, Accessory


def wishlist_view(request) -> HttpResponse:
    wishlist = list(set(request.session.get("wishlist", [])))
    if wishlist:
        try:
            wishlist_ids = [int(id) for id in wishlist]
        except ValueError:
            wishlist_ids = []

        # Fetch existing Items and Accessories
        existing_items = Item.objects.filter(id__in=wishlist_ids).values_list("id", flat=True)
        existing_accessories = Accessory.objects.filter(id__in=wishlist_ids).values_list("id", flat=True)
        valid_wishlist = [id for id in wishlist_ids if id in existing_items or id in existing_accessories]

        # Update session with valid IDs
        request.session["wishlist"] = valid_wishlist
        request.session.modified = True

        # Fetch Item and Accessory objects
        items = Item.objects.filter(id__in=valid_wishlist)
        accessories = Accessory.objects.filter(id__in=valid_wishlist)

        # Combine and sort by created_at
        combined_items = list(items) + list(accessories)
        combined_items.sort(key=lambda x: x.created_at, reverse=True)

        # Paginate combined items
        paginator = Paginator(combined_items, 9)
        page_number = request.GET.get("page")

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    else:
        paginator = Paginator([], 9)
        page_obj = paginator.page(1)

    context = {
        "page_obj": page_obj,
        "wishlist": request.session.get("wishlist", []),
        "meta_description": "AngelDress - Ваш список желаний",
    }
    return render(request, "app_wishlist/wishlist.html", context=context)


def toggle_wishlist(request, dress_id):
    if request.method == "POST":
        wishlist = request.session.get("wishlist", [])

        try:
            obj = Item.objects.get(pk=dress_id)
        except Item.DoesNotExist:
            try:
                obj = Accessory.objects.get(pk=dress_id)
            except Accessory.DoesNotExist:
                return HttpResponse(status=404)

        dress_id = int(dress_id)
        if dress_id in wishlist:
            wishlist.remove(dress_id)
            status = "removed"
            if obj.favorites_count > 0:
                obj.favorites_count -= 1
        else:
            wishlist.append(dress_id)
            status = "added"
            obj.favorites_count += 1

        request.session["wishlist"] = wishlist
        request.session.modified = True

        obj.update_popularity()
        obj.save()

        return JsonResponse({"status": status, "count": len(wishlist)})
    else:
        return HttpResponse(status=400)

def wishlist_count(request):
    wishlist = request.session.get("wishlist", [])
    return JsonResponse({"count": len(wishlist)})
