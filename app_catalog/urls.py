from django.urls import path

from app_catalog.views import catalog_view, product_view

app_name = 'app_catalog'
urlpatterns = [
    path('', catalog_view, name='catalog'),
    path('product/', product_view, name='product'),
]