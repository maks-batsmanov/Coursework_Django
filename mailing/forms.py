from django import forms
from .models import Recipient, Message, Mailing


class FormRecipient(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['full_name', 'email', 'comment']


class FormMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']


