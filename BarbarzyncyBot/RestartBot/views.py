# views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth.decorators import login_required

@login_required
def run_bot(request):
    try:
        call_command('runbot')
        return render(request, 'run_bot.html', {'message': 'Bot successfully started.'})
    except Exception as e:
        return render(request, 'run_bot.html', {'message': f'Error: {str(e)}'})