from django import forms
from .models import RentalRequest

class RentalRequestForm(forms.ModelForm):
    class Meta:
        model = RentalRequest
        fields = ['name', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя и Фамилия'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }