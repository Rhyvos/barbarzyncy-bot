from django.urls import path
from .views import welcome_message_view

urlpatterns = [
    path('welcome-message/', welcome_message_view, name='welcome-message'),
]