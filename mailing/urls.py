from django.urls import path
from .views import *


app_name = 'mailing'

urlpatterns = [

    path('recipient/list/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/update/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/detail/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),

    path('message/list/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('list/', MailingListView.as_view(), name='list'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/', MailingDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),

    path('<int:pk>/send/', SendMailingView.as_view(), name='send'),
    path('logs/', MailingLogListView.as_view(), name='log_list'),
]