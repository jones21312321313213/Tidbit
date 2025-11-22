from django.urls import path
from . import views

urlpatterns = [
    path('deck/', views.DeckListView.as_view(), name='deck_list'),
    path('<slug:slug>/', views.DeckUpdateView.as_view(), name='deck_detail'),
]