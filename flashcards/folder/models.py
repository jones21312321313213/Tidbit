from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    FolderID = models.AutoField(primary_key=True)   
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class Note(models.Model):
    NoteID = models.AutoField(primary_key=True)     
    field_data = models.CharField(max_length=255)  
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="notes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.field_data
