from django import forms
from ckeditor.widgets import CKEditorWidget

from app_catalog.models import Item, Accessory

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'description': CKEditorWidget(),
        }


class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = '__all__'
        widgets = {
            'description': CKEditorWidget(),
        }