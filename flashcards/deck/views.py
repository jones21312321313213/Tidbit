from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
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

        return render(request, self.template_name, {'deck': deck})

    




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
