from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from .models import Deck
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

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


class DeckListView(ListView):
    template_name = 'deck/deck_view.html'

    def get(self,request):
        # # Get all decks for the logged-in user
        # decks = Deck.objects.filter(user=request.user).order_by('-created_at')
        # return render(request, self.template_name, {'decks': decks})
        return render(request, self.template_name)

    


class DeckUpdateView(View):

    def get_url(self):
        return redirect(reverse('review', kwargs={'slug': self.kwargs['slug']}))
    # template_name = 'todo'
    #
    # def get(self, request, pk):
    #     return HttpResponse(f'Viewing deck {pk}')
