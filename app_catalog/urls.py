from django.urls import path

from app_catalog.views import (
    item_catalog_view,
    item_detail_view, accessory_catalog_view, accessory_detail_view,
    yml_feed_view,
)

app_name = 'app_catalog'
urlpatterns = [
    path("", item_catalog_view, name="items_catalog"),
    path("item/<int:dress_id>/", item_detail_view, name="item_detail"),

    path("accessories/", accessory_catalog_view, name="accessory_catalog"),
    path("accessories/item/<int:accessory_id>/", accessory_detail_view, name="accessory_detail"),
    
    # YML-фид для поисковых систем
    path("yml-feed/", yml_feed_view, name="yml_feed"),
]
