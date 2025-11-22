from django.urls import path
from . import views

urlpatterns =[
    path('folder/', views.index, name='folder'),
    path('folder/add', views.add_folder, name='add'),
]