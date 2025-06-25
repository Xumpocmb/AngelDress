from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app_home.urls")),
    path("catalog/", include("app_catalog.urls")),
    path("blog/", include("app_blog.urls")),
    path("wishlist/", include("app_wishlist.urls")),
    path("book/", include("app_book.urls")),
    path("callback/", include("app_client_call_back.urls")),
    path("newsletter/", include("app_newsletter.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
