from django.contrib import admin, messages
from django.core.exceptions import ObjectDoesNotExist

from .models import Subscriber, Newsletter
from django.utils.html import format_html
from django.urls import reverse, NoReverseMatch, path
from django.http import HttpResponseRedirect

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)



@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'sent', 'action_buttons')

    def action_buttons(self, obj):
        if not obj.sent:
            url = f"/admin/app_newsletter/newsletter/{obj.id}/send/"
            return format_html('<a class="button" href="{}">Отправить рассылку</a>', url)
        return "-"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:newsletter_id>/send/',
                 self.admin_site.admin_view(self.send_newsletter),
                 name='admin_send_newsletter'),
        ]
        return custom_urls + urls

    def send_newsletter(self, request, newsletter_id):
        try:
            newsletter = Newsletter.objects.get(pk=newsletter_id)
            newsletter.send()
            self.message_user(request, "✅ Рассылка успешно отправлена всем подписчикам.", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"❌ Ошибка при отправке рассылки: {e}", level=messages.ERROR)
        url = reverse('admin:app_newsletter_newsletter_change', args=[newsletter_id])
        return HttpResponseRedirect(url)

