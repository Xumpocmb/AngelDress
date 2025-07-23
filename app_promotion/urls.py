from django.urls import path
from .views import promotions_list, promotion_detail

app_name = 'app_promotion'

urlpatterns = [
    path('', promotions_list, name='promotions_list'),
    path('<int:promotion_id>/', promotion_detail, name='promotion_detail'),
]