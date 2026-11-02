from datetime import timezone
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from .forms import *
from django.utils import timezone
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .services import send_mailing




class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        context['total_mailings'] = Mailing.objects.count()
        context['total_recipients'] = Recipient.objects.count()
        context['active_mailings'] = sum(
            1 for m in Mailing.objects.all()
            if m.start_time <= now <= m.end_time and m.status == 'Запущена'
        )
        return context


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = FormRecipient
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = FormRecipient
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')


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


class MessageCreateView(CreateView):
    model = Message
    form_class = FormMessage
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = FormMessage
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'
    paginate_by = 10


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('mailing:message_list')


class MailingCreateView(CreateView):
    model = Mailing
    form_class = FormMailing
    template_name = 'mailing/form.html'
    success_url = reverse_lazy('mailing:list')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = FormMailing
    template_name = 'mailing/form.html'
    success_url = reverse_lazy('mailing:list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/list.html'
    context_object_name = 'mailings'
    paginate_by = 10


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/detail.html'
    context_object_name = 'mailing'


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/delete.html'
    context_object_name = 'mailing'
    success_url = reverse_lazy('mailing:list')


class SendMailingView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        result = send_mailing(mailing)

        if result['error']:
            messages.error(request, f"Ошибка: {result['error']}")
        else:
            messages.success(
                request,
                f"Рассылка завершена. Успешно: {result['success']}, "
                f"Не успешно: {result['failed']}"
            )
        return redirect('mailing:detail', pk=pk)


class MailingLogListView(ListView):
    model = MailingLog
    template_name = 'mailing/attempt_list.html'
    context_object_name = 'logs'
    paginate_by = 20
    ordering = ['-datetime']