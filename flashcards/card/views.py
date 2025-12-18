from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
import django.urls
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import UpdateView, ListView, DeleteView

from card.forms import BasicCardForm, IdentificationCardForm, ImageOcclusionCardForm
from card.models import Card, BasicCard, IdentificationCard, ImageOcclusionCard
from deck.models import Deck
from user.models import User as CustomUser

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    success_url = reverse_lazy('card_browse')

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

class BaseCardView(LoginRequiredMixin, View):
    form_class = None
    template_name = 'card/card_create.html'
    card_type = None

    def get(self, request, slug):
        deck = get_object_or_404(Deck, slug=slug, user__username=request.user.username)
        user_decks = Deck.objects.filter(user__username=request.user.username).order_by('-created_at')
        form = self.form_class()

        context = {'form': form,'deck': deck,'user_decks': user_decks, 'card_type': self.card_type}
        return render(request, self.template_name, context)

    def post(self, request, slug):
        custom_user = get_object_or_404(CustomUser, username=request.user.username)
        deck = get_object_or_404(Deck, slug=slug, user__username=request.user.username)
        user_decks = Deck.objects.filter(user__username=request.user.username).order_by('-created_at')
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.user = custom_user
            card.save()

            if self.card_type == 'image':
                return redirect('create_image_card', slug=slug)
            elif self.card_type == 'identification':
                return redirect('create_identification_card', slug=slug)
            else:
                return redirect('create_basic_card', slug=slug)

        context = {'form': form,'deck': deck,'user_decks': user_decks,'card_type': self.card_type}
        return render(request, self.template_name, context)

class ImageCardView(BaseCardView):
    form_class = ImageOcclusionCardForm
    card_type = 'image'

class IdentificationCardView(BaseCardView):
    form_class = IdentificationCardForm
    card_type = 'identification'

class BasicCardView(BaseCardView):
    form_class = BasicCardForm
    card_type = 'basic'

class CardEditView(LoginRequiredMixin, UpdateView):
    template_name = 'card/card_edit.html'
    context_object_name = 'card'

    def get_object(self, queryset=None):
        card = get_object_or_404(Card, pk=self.kwargs['pk'], user__username=self.request.user)

        if hasattr(card, 'basiccard'):
            return card.basiccard
        elif hasattr(card, 'identificationcard'):
            return card.identificationcard
        elif hasattr(card, 'imageocclusioncard'):
            return card.imageocclusioncard
        return card

    def get_form_class(self):
        obj = self.get_object()
        if isinstance(obj, BasicCard):
            return BasicCardForm
        elif isinstance(obj, IdentificationCard):
            return IdentificationCardForm
        elif isinstance(obj, ImageOcclusionCard):
            return ImageOcclusionCardForm
        return BasicCardForm

    def get_success_url(self):
        return django.urls.reverse('review', kwargs={'slug': self.object.deck.slug})

class CardBrowseView(LoginRequiredMixin, ListView):
    model = Card
    template_name = 'card/card_browse.html'
    context_object_name = 'cards'
    paginate_by = 30

    def get_queryset(self):
        custom_user = get_object_or_404(CustomUser, username=self.request.user.username)

        # Filter cards by the CustomUser, not request.user
        queryset = Card.objects.filter(user=custom_user).select_related('deck')

        # Filter by Deck
        deck_slug = self.request.GET.get('deck')
        if deck_slug:
            queryset = queryset.filter(deck__slug=deck_slug)

        # Filter by Search (Front Field)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(front_field__icontains=search_query)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        custom_user = get_object_or_404(CustomUser, username=self.request.user.username)

        # Fix: Filter decks using the custom_user as well
        context['decks'] = Deck.objects.filter(user=custom_user)

        context['current_deck'] = self.request.GET.get('deck', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context