from django.urls import path
from .views import bot_settings_view

urlpatterns = [
    path('bot-settings/', bot_settings_view, name='bot-settings-view'),
]