from datetime import timezone
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from .forms import *
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .services import send_mailing


@method_decorator(cache_page(60 * 15), name='dispatch')
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

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipient
    form_class = FormRecipient
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def test_func(self):
        recipient = self.get_object()
        return recipient.owner == self.request.user


class RecipientListView(ListView):
    model = Recipient
    template_name = 'mailing/recipients_list.html'
    context_object_name = 'recipients'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджеры').exists():
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Recipient
    template_name = 'mailing/recipient_detail.html'
    context_object_name = 'recipient'

    def test_func(self):
        recipient = self.get_object()
        return (
                recipient.owner == self.request.user
                or self.request.user.groups.filter(name='Менеджеры').exists()
        )


class RecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_delete.html'
    context_object_name = 'recipient'
    success_url = reverse_lazy('mailing:recipients_list')

    def test_func(self):
        recipient = self.get_object()
        return recipient.owner == self.request.user


class MessageCreateView(CreateView):
    model = Message
    form_class = FormMessage
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = FormMessage
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def test_func(self):
        recipient = self.get_object()
        return recipient.owner == self.request.user


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджеры').exists():
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'

    def test_func(self):
        recipient = self.get_object()
        return (
                recipient.owner == self.request.user
                or self.request.user.groups.filter(name='Менеджеры').exists()
        )


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('mailing:message_list')

    def test_func(self):
        recipient = self.get_object()
        return recipient.owner == self.request.user


class MailingCreateView(CreateView):
    model = Mailing
    form_class = FormMailing
    template_name = 'mailing/form.html'
    success_url = reverse_lazy('mailing:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = FormMailing
    template_name = 'mailing/form.html'
    success_url = reverse_lazy('mailing:list')

    def test_func(self):
        recipient = self.get_object()
        return recipient.owner == self.request.user

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/list.html'
    context_object_name = 'mailings'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        cache_key = f'mailings_user_{user.id}'

        queryset = cache.get(cache_key)
        if queryset is None:
            # Если менеджер — все, иначе — только свои
            if user.groups.filter(name='Менеджеры').exists():
                queryset = Mailing.objects.all()
            else:
                queryset = Mailing.objects.filter(owner=user)
            cache.set(cache_key, queryset, 60 * 5)  # 5 минут

        return queryset


class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    template_name = 'mailing/detail.html'
    context_object_name = 'mailing'

    def test_func(self):
        recipient = self.get_object()
        return (
                recipient.owner == self.request.user
                or self.request.user.groups.filter(name='Менеджеры').exists()
        )


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/delete.html'
    context_object_name = 'mailing'
    success_url = reverse_lazy('mailing:list')

    def test_func(self):
        recipient = self.get_object()
        return recipient.owner == self.request.user


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


class StatsView(TemplateView):
    template_name = 'mailing/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.groups.filter(name='Менеджеры').exists():
            mailings = Mailing.objects.all()
        else:
            mailings = Mailing.objects.filter(owner=user)

        logs = MailingLog.objects.filter(mailing__in=mailings)

        context['success_count'] = logs.filter(status=MailingLog.STATUS_SUCCESS).count()
        context['failed_count'] = logs.filter(status=MailingLog.STATUS_FAILURE).count()
        context['total_sent'] = logs.count()
        context['total_mailings'] = mailings.count()

        return context


class ToggleMailingView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Менеджеры').exists()

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_disabled = not mailing.is_disabled
        mailing.save()
        messages.success(
            request,
            f'Рассылка #{mailing.pk} {"отключена" if mailing.is_disabled else "включена"}'
        )
        return redirect('mailing:list')