from django.urls import path
from app_book.views import create_rental_request

app_name = 'app_book'
urlpatterns = [
    path('create/', create_rental_request, name='create_rental_request'),
]