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

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        import re
        cleaned_phone = re.sub(r'[^\d+]', '', phone.strip())
        if not re.match(r'^\+?\d{10,15}$', cleaned_phone):
            raise forms.ValidationError("Неверный формат номера телефона")
        return cleaned_phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower().strip()