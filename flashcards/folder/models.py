"""from django.db import models

from user.models import User
# Create your models here.
class Folder(models.Model):
    folderId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)

    def __str__(self):
        return f"{self.folderId} {self.name} {self.created_at} {self.user.username}"

class Note(models.Model):
    noteId = models.AutoField(primary_key=True)
    field_data = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.noteId} {self.field_data} {self.created_at} {self.folder.name}"""
from django.db import models
from user.models import User

class Folder(models.Model):
    folderId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        user_name = self.user.username if self.user else "No User"
        return f"{self.folderId} {self.name} {self.created_at} {user_name}"

class Note(models.Model):
    noteId = models.AutoField(primary_key=True)
    field_data = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.noteId} {self.field_data} {self.created_at} {self.folder.name}"