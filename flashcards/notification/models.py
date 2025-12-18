from django.db import models
from django.conf import settings
from card.models import Card

class Notification(models.Model):
    notificationId = models.AutoField(primary_key=True)
    description = models.CharField(max_length=128)
    status = models.BooleanField(default=False)
    schedule = models.DateTimeField(auto_now_add=True)
    # Reference the custom User model via settings
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.notificationId} - {self.description}"