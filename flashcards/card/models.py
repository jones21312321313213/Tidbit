from django.db import models
from django.utils import timezone
from deck.models import Deck
from user.models import User


class Card(models.Model):
    class State(models.IntegerChoices):
        NEW = 0
        LEARNING = 1
        REVIEW = 2
        RELEARNING = 3

    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stability = models.FloatField(default=0)
    difficulty = models.FloatField(default=0)
    state = models.IntegerField(choices=State.choices, default=State.NEW)
    last_review = models.DateTimeField(null=True, blank=True)
    next_review = models.DateTimeField(default=timezone.now)
    step = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card {self.id} (Due:{self.next_review:.2f})"

    # Placeholder method to change the schedule based on a spaced-repetition algorithm
    def update_schedule(self, performance_rating):
        pass

class BasicCard(Card):
    front_field = models.TextField()
    back_field = models.TextField()

class IdentificationCard(Card):
    hidden_field = models.TextField()

class ImageOcclusionCard(Card):
    img_path = models.ImageField(upload_to='occlusion_images/')