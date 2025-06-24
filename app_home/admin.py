from django.contrib import admin
from django.db import models
from django.forms import Textarea
from app_home.forms import RentRulesForm
from app_home.models import SliderImage, ContactInfo, RentRules


class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'alt_text', 'order')
    list_editable = ('order',)
    readonly_fields = ('image_tag',)


class ContactInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()

admin.site.register(SliderImage, SliderImageAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)


@admin.register(RentRules)
class RentRulesAdmin(admin.ModelAdmin):
    form = RentRulesForm

    def has_add_permission(self, request):
        return not RentRules.objects.exists()
