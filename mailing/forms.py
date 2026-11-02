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


class FormMailing(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'status', 'message', 'recipients']

        widgets = {
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Select(attrs={'class': 'form-select'}),
            'recipients': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
        labels = {
            'start_time': 'Дата и время начала',
            'end_time': 'Дата и время окончания',
            'status': 'Статус',
            'message': 'Сообщение',
            'recipients': 'Получатели',
        }