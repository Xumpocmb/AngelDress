from django.urls import path

from app_wishlist.views import wishlist_view

app_name = 'app_wishlist'
urlpatterns = [
    path('', wishlist_view, name='wishlist'),
]