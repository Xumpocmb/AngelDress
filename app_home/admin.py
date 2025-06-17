from django.contrib import admin
from app_home.models import SliderImage


class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'alt_text', 'order')
    list_editable = ('order',)
    readonly_fields = ('image_tag',)


admin.site.register(SliderImage, SliderImageAdmin)