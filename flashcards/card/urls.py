from django.urls import path

from card.views import CreateCardView, AddCardView

# from .views import AnswerCardView, ReviewDeckView

urlpatterns = [
    path('<slug:slug>/study', CreateCardView.as_view(), name='review'),
    path('add/', AddCardView.as_view(), name='add')
]