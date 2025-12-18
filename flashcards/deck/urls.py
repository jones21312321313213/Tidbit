from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.DeckCreateView.as_view(), name='deck_create'),
    path('<slug:slug>/edit/', views.DeckUpdateView.as_view(), name='deck_update'),
    path('<slug:slug>/delete/', views.DeckDeleteView.as_view(), name='deck_delete'),
    path('<slug:slug>/review/', views.ReviewView.as_view(), name='review'),
]
