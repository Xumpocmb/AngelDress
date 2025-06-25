from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import RentRules, TermsOfUse


class RentRulesForm(forms.ModelForm):
    class Meta:
        model = RentRules
        fields = "__all__"
        widgets = {"text": CKEditorWidget()}


class TermsOfUseForm(forms.ModelForm):
    class Meta:
        model = TermsOfUse
        fields = "__all__"
        widgets = {"text": CKEditorWidget()}
