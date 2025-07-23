from django.urls import path

from app_blog.views import blog_view, post_view, posts_by_tag

app_name = 'app_blog'
urlpatterns = [
    path('', blog_view, name='blog'),
    path('post/<int:post_id>/', post_view, name='post'),
    path('tag/<slug:tag_slug>/', posts_by_tag, name='posts_by_tag'),
]