from django.urls import path
from .views import update_bot

urlpatterns = [
    path('update/', update_bot, name='update-bot'),
]