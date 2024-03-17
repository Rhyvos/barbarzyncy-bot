import os
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from dotenv import dotenv_values
from django.conf import settings as project_settings
from django.contrib.auth.decorators import login_required

settings = dotenv_values(project_settings.ENV_PATH)
    
@login_required
def logs_view(request):
    log_entries = []
    log_file_path = os.path.join(settings['LOGS_DIR'], 'bot_status.log')
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            log_entries = [line.rstrip('\r\n') for line in lines[-100:]]
            log_entries = '\n'.join(log_entries)
    except Exception as e:
        return render(request, 'view_logs.html', {'log_entries': '', 'error_message': e})
    
    context = {
        'log_entries': log_entries,
    }

    return render(request, 'view_logs.html', context)

@login_required
def download_logs(request):
    # Pobierz cały plik logów
    print('Downloading logs')
    log_file_path = os.path.join(settings['LOGS_DIR'], 'bot_status.log')
    with open(log_file_path, 'r') as f:
        response = HttpResponse(f.read(), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="bot_status.log"'
    return response