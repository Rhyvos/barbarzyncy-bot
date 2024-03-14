from django import forms
from .models import WelcomeMessage

class WelcomeMessageForm(forms.ModelForm):
    class Meta:
        model = WelcomeMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }
        labels = {
            "message": "Wiadomość powitalna",
        }