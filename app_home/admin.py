from django.contrib import admin
from app_home.forms import RentRulesForm, TermsOfUseForm
from app_home.models import NewsTicker, SliderImage, ContactInfo, RentRules, TermsOfUse, Questions, Counter


class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'alt_text', 'order')
    list_editable = ('order',)
    readonly_fields = ('image_tag',)


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ["type", "title", "link", "is_active"]
    list_editable = ["is_active"]

admin.site.register(SliderImage, SliderImageAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)


@admin.register(RentRules)
class RentRulesAdmin(admin.ModelAdmin):
    form = RentRulesForm

    def has_add_permission(self, request):
        return not RentRules.objects.exists()


@admin.register(TermsOfUse)
class TermsOfUseAdmin(admin.ModelAdmin):
    form = TermsOfUseForm

    def has_add_permission(self, request):
        return not TermsOfUse.objects.exists()


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'is_active')
    list_editable = ('is_active',)


@admin.register(NewsTicker)
class NewsTickerAdmin(admin.ModelAdmin):
    list_display = ("text", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("text",)


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'label')
    list_editable = ('value',)