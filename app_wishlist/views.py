from django.shortcuts import render

def wishlist_view(request):
    return render(request, 'app_wishlist/wishlist.html')
