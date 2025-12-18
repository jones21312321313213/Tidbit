from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(models.Model):
    userId = models.AutoField(primary_key=True, unique=True) # or userId = models.IntegerField(primary_key=True) choose which is correct
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length= 100, unique=True)# or email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.userId} {self.username} {self.email}"