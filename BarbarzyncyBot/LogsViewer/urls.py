from django.urls import path
from .views import download_logs, logs_view


urlpatterns = [
    path('view-logs/', logs_view, name='view-logs'),
    path('download-logs/', download_logs, name='download-logs'),
]