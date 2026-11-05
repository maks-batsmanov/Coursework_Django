from django.contrib import admin
from django.urls import path, include

from mailing.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('mailing/', include('mailing.urls', namespace='mailing')),
    path('users/', include('users.urls', namespace='users'))
]
