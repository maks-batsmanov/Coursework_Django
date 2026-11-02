from django import forms
from .models import Recipient, Message, Mailing


class FormRecipient(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['full_name', 'email', 'comment']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'full_name': 'ФИО',
            'email': 'Email',
            'comment': 'Комментарий',
        }


class FormMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

        widgets = {
                    'subject': forms.TextInput(attrs={'class': 'form-control'}),
                    'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                }
        labels = {
            'subject': 'Тема',
            'body': 'Сообщение',
        }