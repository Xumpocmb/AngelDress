from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from app_book.models import RentalRequest

class DressInline(admin.TabularInline):
    model = RentalRequest.dresses.through
    extra = 0
    verbose_name = "Платье"
    verbose_name_plural = "Бронируемые платья"

    raw_id_fields = ['dress']
    readonly_fields = ['public_url']

    def public_url(self, instance):
        """Ссылка на платье на сайте."""
        if instance and instance.dress:
            url = reverse('app_catalog:dress_detail', kwargs={'dress_id': instance.dress.id})
            return format_html('<a href="{}" target="_blank">Посмотреть на сайте</a>', url)
        return ''

    public_url.short_description = "Посмотреть на сайте"


@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('created_at',)

    inlines = [DressInline]
