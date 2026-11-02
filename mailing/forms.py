from django import forms
from .models import Recipient, Message, Mailing


class FormRecipient(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['full_name', 'email', 'comment']


        # labels = {
        #     'full_name': 'Имя и фамилию',
        #     'email': 'E-mail',
        #     'comment': 'Комментарий',
        # }

