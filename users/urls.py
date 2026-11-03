from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, UserListView, ToggleBlockUserView
from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

urlpatterns += [
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/toggle-block/', ToggleBlockUserView.as_view(), name='toggle_block'),
]