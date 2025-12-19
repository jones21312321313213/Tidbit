from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeckUpdateView.as_view(), name='deck_list'),
    path('create/', views.DeckCreateView.as_view(), name='deck_create'),
    path('<slug:slug>/', views.DeckListView.as_view(), name='deck_detail'),
    path('<slug:slug>/delete/', views.DeckDeleteView.as_view(), name='deck_delete'),
]
