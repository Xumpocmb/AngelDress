from django.urls import path

from app_home.views import index_view, contact_view

app_name = 'app_home'
urlpatterns = [
    path('', index_view, name='home'),
    path('contacts/', contact_view, name='contacts'),
]