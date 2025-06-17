from django.contrib import admin
from app_home.models import SliderImage, ContactInfo


class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'alt_text', 'order')
    list_editable = ('order',)
    readonly_fields = ('image_tag',)


class ContactInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()

admin.site.register(SliderImage, SliderImageAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)