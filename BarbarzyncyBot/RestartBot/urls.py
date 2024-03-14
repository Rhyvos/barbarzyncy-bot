from django.urls import path
from .views import run_bot

urlpatterns = [
    # Inne ścieżki...
    path('runbot/', run_bot, name='run-bot'),
]