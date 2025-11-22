from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from .models import Folder

# Display all folders
def index(request):
    folders = Folder.objects.all()
    #return HttpResponse("hello")
    return render(request, 'folder/index.html', {'folders': folders})

# Login page for folder app (if needed)
def add_folder(request):
    #return render(request, 'folder/add.html')
    return HttpResponse("hello")



