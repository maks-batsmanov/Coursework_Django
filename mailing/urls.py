from django.urls import path
from .views import RecipientCreateView, RecipientUpdateView, RecipientListView, RecipientDeleteView, RecipientDetailView


app_name = 'mailing'

urlpatterns = [

    path('recipient/list/', RecipientListView.as_view(), name='recipients_list'),
    path('recipient/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/update/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/detail/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),

]