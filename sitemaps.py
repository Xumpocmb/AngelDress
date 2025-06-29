from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from app_blog.models import Post
from app_catalog.models import Dress
from app_home.models import RentRules, TermsOfUse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return [
            'app_home:home',
            'app_home:about',
            'app_home:contacts',
            'app_blog:blog',
            'app_catalog:dress_catalog',
        ]

    def location(self, item):
        return reverse(item)

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.all().order_by('-created_at')

    def location(self, item):
        return reverse('app_blog:post', args=[item.id])

    def lastmod(self, obj):
        return obj.updated_at

class DressSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Dress.objects.all().order_by('-created_at')

    def location(self, item):
        return reverse('app_catalog:dress_detail', args=[item.id])
