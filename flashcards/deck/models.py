from django.db import models
from django.utils.text import slugify

from user.models import User
# Create your models here.
class Deck(models.Model):
    deckId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=120, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.name != getattr(self, '_original_name', None):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        self._original_name = self.name

    def __str__(self):
        return f"{self.deckId} {self.name} {self.description} {self.user.username}"