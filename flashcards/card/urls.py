from django.urls import path

from card.views import ImageCardView, IdentificationCardView, BasicCardView, CardEditView, CardDeleteView, \
    CardBrowseView

urlpatterns = [
    path('deck/<slug:slug>/add/image/', ImageCardView.as_view(), name='create_image_card'),
    path('deck/<slug:slug>/add/identification/', IdentificationCardView.as_view(), name='create_identification_card'),
    path('deck/<slug:slug>/add/basic/', BasicCardView.as_view(), name='create_basic_card'),
    path('card/<int:pk>/edit/', CardEditView.as_view(), name='card_edit'),
    path('cards/browse/', CardBrowseView.as_view(), name='card_browse'),
    path('card/<int:pk>/delete/', CardDeleteView.as_view(), name='card_delete'),
]