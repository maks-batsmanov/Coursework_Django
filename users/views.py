from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm
from django.views import View

User = get_user_model()

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        send_mail(
            subject='Добро пожаловать!',
            message='Спасибо за регистрацию на нашем сервисе рассылок.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.groups.filter(name='Менеджеры').exists()


class ToggleBlockUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Менеджеры').exists()

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            messages().error(request, 'Нельзя заблокировать самого себя')
        else:
            user.is_blocked = not user.is_blocked
            user.save()
            messages.success(request, f'Пользователь {user.email} {"заблокирован" if user.is_blocked else "разблокирован"}')
        return redirect('users:user_list')


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        if user.is_blocked:
            messages.error(self.request, 'Ваш аккаунт заблокирован. Обратитесь к менеджеру.')
            return redirect('users:login')
        return super().form_valid(form)