from django.urls import path

from app_wishlist.views import wishlist_view, toggle_favorite, get_wishlist_count

app_name = 'app_wishlist'
urlpatterns = [
    path('', wishlist_view, name='wishlist'),
    path('api/toggle/<int:dress_id>/', toggle_favorite, name='toggle_favorite'),
    path('api/count/', get_wishlist_count, name='get_wishlist_count'),
]
