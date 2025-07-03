from django.urls import path

from app_catalog.views import (
    item_catalog_view,
    item_detail_view,
)

app_name = 'app_catalog'
urlpatterns = [
    path("", item_catalog_view, name="dress_catalog"),
    path("item/<int:dress_id>/", item_detail_view, name="dress_detail"),
]
