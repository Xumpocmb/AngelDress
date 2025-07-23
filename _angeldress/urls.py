from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from sitemaps import (
    StaticViewSitemap,
    PostSitemap,
    DressSitemap,
)

sitemaps = {
    'static': StaticViewSitemap,
    'posts': PostSitemap,
    'dresses': DressSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app_home.urls")),
    path("catalog/", include("app_catalog.urls")),
    path("blog/", include("app_blog.urls")),
    path("wishlist/", include("app_wishlist.urls")),
    path("book/", include("app_book.urls")),
    path("callback/", include("app_client_call_back.urls")),
    path("newsletter/", include("app_newsletter.urls")),
    path("promo/", include("app_promotion.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap",),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
