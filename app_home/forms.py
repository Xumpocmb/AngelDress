from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import RentRules


class RentRulesForm(forms.ModelForm):
    class Meta:
        model = RentRules
        fields = "__all__"
        widgets = {
            "text": CKEditorWidget(),
        }
