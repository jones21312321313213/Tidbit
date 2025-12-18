from django.db import models
from django.utils import timezone
from deck.models import Deck
from user.models import User
from fsrs import Card as FSRS_Card, State as FSRS_State
from card.scheduler import Scheduler

class Card(models.Model):
    class State(models.IntegerChoices):
        New = 0
        Learning = 1
        Review = 2
        Relearning = 3

    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    stability = models.FloatField(default=0)
    difficulty = models.FloatField(default=0)
    state = models.IntegerField(choices=State.choices, default=State.New)
    last_review = models.DateTimeField(null=True, blank=True)
    next_review = models.DateTimeField(default=timezone.now)
    step = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    front_field = models.TextField(null=True, blank=True)

    def update_schedule(self, rating):
        if self.state == Card.State.New:
            FSRSCard = FSRS_Card()
        else:
            FSRSCard = FSRS_Card(
                state=FSRS_State(self.state),
                stability=self.stability,
                difficulty=self.difficulty,
                step=self.step if self.step is not None else 0,
                due=self.next_review,
                last_review=self.last_review
            )

        scheduler = Scheduler()
        FSRSCard_new, reviewLog = scheduler.review_card(FSRSCard, rating)

        self.state = FSRSCard_new.state
        self.stability = FSRSCard_new.stability
        self.difficulty = FSRSCard_new.difficulty
        self.step = FSRSCard_new.step
        self.next_review = FSRSCard_new.due
        self.last_review = FSRSCard_new.last_review
        self.save()

class BasicCard(Card):
    back_field = models.TextField()

class IdentificationCard(Card):
    hidden_field = models.TextField()

class ImageOcclusionCard(Card):
    img_path = models.ImageField(upload_to='static/card/occlusion_images/')