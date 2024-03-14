from django.db import models

class WelcomeMessage(models.Model):
    message = models.TextField()

    def __str__(self):
        return "Wiadomość powitalna"