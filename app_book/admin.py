from urllib.parse import quote_plus

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from app_book.forms import RentalRequestForm
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
    list_display = ('id', 'name', 'phone', 'email', 'status', 'created_at', 'whatsapp_button')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('created_at',)
    list_editable = ("status",)
    inlines = [DressInline]

    def whatsapp_button(self, obj):
        phone_clean = ''.join(filter(str.isdigit, obj.phone))

        if not phone_clean:
            return "-"

        dress_names = ", ".join([str(dress) for dress in obj.dresses.all()])
        message = (
            f"Здравствуйте, {obj.name}!\n"
            f"Спасибо за заявку №{obj.id} на примерку следующих платьев: {dress_names}.\n"
            f"Мы свяжемся с вами в ближайшее время."
        )
        encoded_message = quote_plus(message)

        wa_link = f"https://wa.me/{phone_clean}?text={encoded_message}"

        return format_html(
            '<a href="{0}" target="_blank" style="padding: 5px 10px; background: #25D366; color: white; text-decoration: none; border-radius: 4px;">' 
            '💬 WhatsApp</a>',
            wa_link
        )

    whatsapp_button.short_description = "WhatsApp"
    whatsapp_button.allow_tags = True
