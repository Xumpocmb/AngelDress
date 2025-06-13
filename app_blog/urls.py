from django.urls import path

from app_blog.views import blog_view

app_name = 'app_blog'
urlpatterns = [
    path('', blog_view, name='blog'),
]