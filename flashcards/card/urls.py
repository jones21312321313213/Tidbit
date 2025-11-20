from django.urls import path

from card.views import CreateCardView

# from .views import AnswerCardView, ReviewDeckView

urlpatterns = [
    path('<slug:slug>/study', CreateCardView.as_view(), name='review')
]