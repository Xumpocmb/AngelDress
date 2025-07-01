from django.urls import path

from app_catalog.views import (
    dress_catalog_view,
    dress_detail_view,
    accesory_catalog_view,
    accesory_detail_view,
)

app_name = 'app_catalog'
urlpatterns = [
    path("", dress_catalog_view, name="dress_catalog"),
    path("dress/<int:dress_id>/", dress_detail_view, name="dress_detail"),
    path("accessories/", accesory_catalog_view, name="accessories"),
    path(
        "accessory/<int:accessory_id>/", accesory_detail_view, name="accessory_detail"
    ),
]
