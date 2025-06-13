from django.urls import path

from app_news.views import news_view

app_name = 'app_news'
urlpatterns = [
    path('', news_view, name='news'),
]