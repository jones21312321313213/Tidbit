from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Folder, Note


@login_required(login_url='login')
def folder_create(request):
    if request.method == 'POST':
        name = request.POST.get('folder_name')
        if name:
            Folder.objects.create(name=name)
            messages.success(request, f"Folder '{name}' created successfully!")
            return redirect('home')
    return render(request, 'folder/folder_create.html')


@login_required(login_url='login')
def folder_edit(request, FolderID):
    folder = get_object_or_404(Folder, FolderID=FolderID)
    if request.method == 'POST':
        new_name = request.POST.get('folder_name')
        if new_name:
            folder.name = new_name
            folder.save()
            messages.success(request, f"Folder renamed to '{new_name}'")
            return redirect('home')
    return render(request, 'folder/folder_edit.html', {'folder': folder})


@login_required(login_url='login')
def note_create(request):
    if request.method == 'POST':
        field_data = request.POST.get('field_data') 
        folder_id = request.POST.get('folder_id')
        folder = get_object_or_404(Folder, FolderID=folder_id)  
        if field_data:
            Note.objects.create(field_data=field_data, folder=folder)
            messages.success(request, f"Note '{field_data}' created in folder '{folder.name}'")
            return redirect('home')
    folders = Folder.objects.all()
    return render(request, 'folder/note_create.html', {'folders': folders})



@login_required(login_url='login')
def folder_edit_dropdown(request):
    if request.method == 'POST':
        folder_id = request.POST.get('folder_id')
        new_name = request.POST.get('folder_name')
        if folder_id and new_name:
            folder = get_object_or_404(Folder, FolderID=folder_id)
            folder.name = new_name
            folder.save()
            messages.success(request, f"Folder renamed to '{new_name}'")
            return redirect('home')
        else:
            messages.error(request, "Please select a folder and enter a new name.")
            return redirect('home')


@login_required(login_url='login')
def folder_delete(request, FolderID):
    folder = get_object_or_404(Folder, FolderID=FolderID)
    if request.method == 'POST':
        folder.delete()
        messages.success(request, f"Folder '{folder.name}' deleted successfully!")
        return redirect('home')
    return render(request, 'folder/folder_delete.html', {'folder': folder})
