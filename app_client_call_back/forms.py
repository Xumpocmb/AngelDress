from django import forms
from .models import ClientCallBack


class ClientCallBackForm(forms.ModelForm):
    agreement = forms.BooleanField(required=True, error_messages={
        'required': 'Необходимо принять условия обработки данных.'
    })

    class Meta:
        model = ClientCallBack
        fields = ['name', 'phone', 'email', 'agreement']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'Имя и Фамилия',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'Номер телефона',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form_input',
                'placeholder': 'Email',
                'required': True,
            }),
        }

        error_messages = {
            'name': {
                'required': 'Укажите имя и фамилию.',
            },
            'phone': {
                'required': 'Укажите номер телефона.',
            },
            'email': {
                'required': 'Укажите email.',
                'invalid': 'Введите корректный email.',
            },
        }
