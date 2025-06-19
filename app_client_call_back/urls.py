from django.urls import path
from .views import ajax_callback_view

urlpatterns = [
    path('ajax/', ajax_callback_view, name='callback_ajax'),
]
