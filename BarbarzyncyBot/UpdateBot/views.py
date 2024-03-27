# views.py
from django.shortcuts import render
from django.core.management import call_command
from django.contrib.auth.decorators import login_required

@login_required
def update_bot(request):
    try:
        ret = call_command('update')
        return render(request, 'update_bot.html', {'message': ret})
    except Exception as e:
        return render(request, 'update_bot.html', {'message': f'{e.__class__.__name__}: {str(e)}'})
