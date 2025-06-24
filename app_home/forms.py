from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import RentRules


class RentRulesForm(forms.ModelForm):
    class Meta:
        model = RentRules
        fields = "__all__"
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            )
        }
