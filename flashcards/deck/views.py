from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView


class DeckCreateView(CreateView):
    template_name = 'todo'


class DeckListView(ListView):
    template_name = 'todo'



class DeckUpdateView(View):

    def get_url(self):
        return redirect(reverse('review', kwargs={'slug': self.kwargs['slug']}))
    # template_name = 'todo'
    #
    # def get(self, request, pk):
    #     return HttpResponse(f'Viewing deck {pk}')