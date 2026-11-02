from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import FormRecipient

from .models import Recipient, Message, Mailing


class RecipientCreateView(CreateView):
    model = Recipient
    form_class =FormRecipient
    template_name = 'mailing/form_recipient.html'
    success_url = reverse_lazy('mailing:recipients_list')


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = FormRecipient
    template_name = 'mailing/form_recipient.html'
    success_url = reverse_lazy('mailing:recipients_list')


class RecipientListView(ListView):
    model = Recipient
    template_name = 'mailing/recipients_list.html'
    context_object_name = 'recipients'
    paginate_by = 10


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'mailing/recipient_detail.html'
    context_object_name = 'recipient'


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_delete.html'
    context_object_name = 'recipient'
    success_url = reverse_lazy('mailing:recipients_list')