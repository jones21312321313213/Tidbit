from datetime import timedelta, datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from card.models import Card
from .models import Deck
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import DeleteView
from user.models import User as CustomUser

class DeckCreateView(LoginRequiredMixin, CreateView):
    model = Deck
    template_name = 'deck/deck_create.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        custom_user = get_object_or_404(CustomUser, username=self.request.user.username)
        form.instance.user = custom_user
        return super().form_valid(form)


class DeckListView(LoginRequiredMixin, View):
    template_name = 'deck/deck_view.html'

    # def get(self,request):
    #     # # Get all decks for the logged-in user
    #     # decks = Deck.objects.filter(user=request.user).order_by('-created_at')
    #     # return render(request, self.template_name, {'decks': decks})
    #     return render(request, self.template_name)

    def get(self, request, slug):
        custom_user = get_object_or_404(
            CustomUser,
            username=request.user.username
        )

        deck = get_object_or_404(
            Deck,
            slug=slug,
            user=custom_user
        )
        new  = Card.objects.filter(deck=deck, state=Card.State.New).count()
        learn = Card.objects.filter(deck=deck,state__in=[1, 3]).count()
        due = Card.objects.filter(deck=deck,state=Card.State.Review,next_review__lte=timezone.now()).count()
        stat = {
            "new_count": new,
            "learn_count": learn,
            "due_count": due,
        }
        return render(request, self.template_name, {'deck': deck, 'stat': stat})

    




class DeckUpdateView(LoginRequiredMixin, UpdateView):
    model = Deck
    template_name = 'deck/deck_edit.html'
    fields = ['name', 'description']  # Fields to update

    def get_object(self, queryset=None):
        # Only allow the owner to edit
        custom_user = get_object_or_404(CustomUser, username=self.request.user.username)
        return get_object_or_404(
            Deck,
            slug=self.kwargs['slug'],
            user=custom_user
        )

    def get_success_url(self):
        # Redirect back to the deck view page after edit
        return reverse('deck_detail', kwargs={'slug': self.object.slug})


class DeckDeleteView(LoginRequiredMixin, DeleteView):

    model = Deck
    success_url = reverse_lazy('home')  # Redirect back to home after deletion

    def get_object(self, queryset=None):
        """Ensure only the logged-in user's deck can be deleted"""
        custom_user = get_object_or_404(CustomUser, username=self.request.user.username)
        return get_object_or_404(
            Deck,
            slug=self.kwargs['slug'],
            user=custom_user
        )

# REVIEWS THE CARDS IN THE DECK
class ReviewView(LoginRequiredMixin, View):
    template_name = 'card/card_review.html'

    def get_next_card(self, deck):
        # GETS THE ALL THE CARDS DUE FOR REVIEW
        card = Card.objects.filter(deck=deck,state__in=[Card.State.New, Card.State.Learning, Card.State.Relearning]).order_by('next_review').first()

        if not card:
            return None

        # DOWNCAST MEANING GI-SPECIALIZE FROM CARD TO BASIC CARD, OR IDENT CARD, OR IMAGE CARD
        if hasattr(card, 'basiccard'):
            return card.basiccard
        elif hasattr(card, 'identificationcard'):
            return card.identificationcard
        elif hasattr(card, 'imageocclusioncard'):
            return card.imageocclusioncard

        return card

    def get(self, request, slug):
        deck = get_object_or_404(Deck, slug=slug, user__username=request.user.username)
        card = self.get_next_card(deck)

        if not card:
            return render(request, 'card/card_finished.html', {'deck': deck})

        context = {'deck': deck,'card': card}
        return render(request, self.template_name, context)

    def post(self, request, slug):
        deck = get_object_or_404(Deck, slug=slug, user__username=request.user.username)

        card_id = request.POST.get('card_id')
        rating = request.POST.get('rating')

        if card_id and rating:
            card = get_object_or_404(Card, id=card_id, deck=deck)
            card.update_schedule(int(rating))
        return redirect('review', slug=slug)