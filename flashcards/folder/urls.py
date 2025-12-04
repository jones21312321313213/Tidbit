from django.urls import path
from . import views

urlpatterns = [
    path("folder/create/", views.folder_create, name="folder_create"),
    path("folder/edit/<int:FolderID>/", views.folder_edit, name="folder_edit"),
    path("note/create/", views.note_create, name="note_create"),
    path("folder/edit-dropdown/", views.folder_edit_dropdown, name="folder_edit_dropdown"),
    path("folder/delete/<int:FolderID>/", views.folder_delete, name="folder_delete"),
]
