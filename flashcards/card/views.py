from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
import django.urls
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import UpdateView, ListView, DeleteView

from card.forms import BasicCardForm, IdentificationCardForm, ImageOcclusionCardForm
from card.models import Card, BasicCard, IdentificationCard, ImageOcclusionCard
from card.procedures import delete_card_proc, create_image_card_proc, create_identification_card_proc, \
    create_basic_card_proc, update_basic_card_proc, update_identification_card_proc, update_image_card_proc
from deck.models import Deck
from user.models import User as CustomUser

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    success_url = reverse_lazy('card_browse')

    def get_queryset(self):
        custom_user = get_object_or_404(CustomUser, username=self.request.user.username)
        return Card.objects.filter(user=custom_user)

    def form_valid(self, form):
        success_url = self.get_success_url()
        delete_card_proc(self.object.pk, self.request.user.username)
        return HttpResponseRedirect(success_url)

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
            user_id = custom_user.userId
            deck_id = deck.deckId
            front = form.cleaned_data.get('front_field')

            if self.card_type == 'image':
                img_path = form.cleaned_data.get('img_path')

                path_str = ''
                if img_path:
                    path_str = default_storage.save(f'static/card/occlusion_images/{img_path.name}', img_path)

                create_image_card_proc(user_id, deck_id, front, path_str)
                return redirect('create_image_card', slug=slug)
            elif self.card_type == 'identification':
                hidden = form.cleaned_data.get('hidden_field')
                create_identification_card_proc(user_id, deck_id, front, hidden)
                return redirect('create_identification_card', slug=slug)

            else:
                back = form.cleaned_data.get('back_field')
                create_basic_card_proc(user_id, deck_id, front, back)
                return redirect('create_basic_card', slug=slug)

        context = {'form': form,'deck': deck,'user_decks': user_decks,'card_type': self.card_type}
        return render(request, self.template_name, context)

class ImageCardView(BaseCardView):
    form_class = ImageOcclusionCardForm
    card_type = 'image'
    template_name = 'card/image_card_create.html'

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

    def form_valid(self, form):
        obj = self.object
        user_id = self.request.user.id
        card_id = obj.id
        front = form.cleaned_data.get('front_field')

        if isinstance(obj, BasicCard):
            back = form.cleaned_data.get('back_field')
            update_basic_card_proc(card_id, user_id, front, back)

        elif isinstance(obj, IdentificationCard):
            hidden = form.cleaned_data.get('hidden_field')
            update_identification_card_proc(card_id, user_id, front, hidden)

        elif isinstance(obj, ImageOcclusionCard):
            img_path = form.cleaned_data.get('img_path')

            if img_path:
                path_str = default_storage.save(f'static/card/occlusion_images/{img_path.name}', img_path)
            else:
                path_str = obj.img_path.name

            update_image_card_proc(card_id, user_id, front, path_str)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return django.urls.reverse('review', kwargs={'slug': self.object.deck.slug})

class CardBrowseView(LoginRequiredMixin, ListView):
    model = Card
    template_name = 'card/card_browse.html'
    context_object_name = 'cards'
    paginate_by = 30

    def get_queryset(self):
        custom_user = get_object_or_404(CustomUser, username=self.request.user.username)
        queryset = Card.objects.filter(user=custom_user).select_related('deck')
        deck_slug = self.request.GET.get('deck')
        if deck_slug:
            queryset = queryset.filter(deck__slug=deck_slug)

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(front_field__icontains=search_query)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        custom_user = get_object_or_404(CustomUser, username=self.request.user.username)

        context['decks'] = Deck.objects.filter(user=custom_user)

        context['current_deck'] = self.request.GET.get('deck', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context