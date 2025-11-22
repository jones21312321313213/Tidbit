from django.urls import path

from card.views import CreateCardView, AddCardView, ViewBack, ViewFront

# from .views import AnswerCardView, ReviewDeckView

urlpatterns = [
    path('<slug:slug>/study', CreateCardView.as_view(), name='review'),
    path('add/', AddCardView.as_view(), name='add'),
    path('review-back', ViewBack.as_view(), name='review-back'),
    path('review-front', ViewFront.as_view(), name='review-front')
]