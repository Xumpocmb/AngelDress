from django.urls import path

from app_wishlist.views import wishlist_view, toggle_wishlist, wishlist_count

app_name = 'app_wishlist'
urlpatterns = [
    path('', wishlist_view, name='wishlist'),
    path('api/toggle/<int:dress_id>/', toggle_wishlist, name='toggle_favorite'),
    path('api/count/', wishlist_count, name='wishlist_count'),

]
