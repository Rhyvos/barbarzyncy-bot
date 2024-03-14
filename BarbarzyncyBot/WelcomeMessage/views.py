from django.shortcuts import render, redirect
from .forms import WelcomeMessageForm
from .models import WelcomeMessage

def welcome_message_view(request):
    if request.method == 'POST':
        form = WelcomeMessageForm(request.POST, instance=WelcomeMessage.objects.first())
        if form.is_valid():
            form.save()
            return redirect('welcome-message')
    else:
        form = WelcomeMessageForm(instance=WelcomeMessage.objects.first())
    return render(request, 'welcome_message_view.html', {'form': form})