from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Count, Q

from .models import Notification
from deck.models import Deck
from card.models import Card, BasicCard, IdentificationCard, ImageOcclusionCard

class NotificationListView(LoginRequiredMixin, View):
    template_name = 'notifications/notification_list.html'
    login_url = 'login'

    def get(self, request):
        auth_user = request.user
        username = getattr(auth_user, 'username', None)
        email = getattr(auth_user, 'email', None)

        # Build Q to match the related project User by username or email
        user_q = Q()
        if username:
            user_q |= Q(user__username=username)
        if email:
            user_q |= Q(user__email=email)

        # Get card state filter parameter
        card_state_filter = request.GET.get('card_state_filter', 'all')

        # Fetch cards that are due for review OR newly created
        now = timezone.now()
        
        if user_q:
            # Get all due cards (cards where next_review is in the past or now)
            # OR newly created cards (state = New)
            due_or_new_cards_qs = Card.objects.filter(
                user_q & (Q(next_review__lte=now) | Q(state=Card.State.New))
            ).select_related('deck', 'user').order_by('next_review')
            
            # Filter by card state if specified
            if card_state_filter != 'all':
                state_map = {
                    'new': Card.State.New,
                    'learning': Card.State.Learning,
                    'review': Card.State.Review,
                    'relearning': Card.State.Relearning,
                }
                if card_state_filter in state_map:
                    due_or_new_cards_qs = due_or_new_cards_qs.filter(state=state_map[card_state_filter])
            
            # Get decks with due card counts (including new cards)
            due_decks = Deck.objects.filter(user_q).annotate(
                due_count=Count('card', filter=Q(card__next_review__lte=now) | Q(card__state=Card.State.New))
            ).filter(due_count__gt=0).order_by('-due_count')
            
            # Total due cards count (including new cards)
            total_due_cards = Card.objects.filter(
                user_q & (Q(next_review__lte=now) | Q(state=Card.State.New))
            ).count()
            
            # Breakdown by card state (including all new cards)
            cards_by_state = {
                'new': Card.objects.filter(user_q & Q(state=Card.State.New)).count(),
                'learning': Card.objects.filter(user_q & Q(next_review__lte=now, state=Card.State.Learning)).count(),
                'review': Card.objects.filter(user_q & Q(next_review__lte=now, state=Card.State.Review)).count(),
                'relearning': Card.objects.filter(user_q & Q(next_review__lte=now, state=Card.State.Relearning)).count(),
            }
        else:
            due_or_new_cards_qs = Card.objects.none()
            due_decks = Deck.objects.none()
            total_due_cards = 0
            cards_by_state = {
                'new': 0,
                'learning': 0,
                'review': 0,
                'relearning': 0,
            }

        context = {
            'due_cards': due_or_new_cards_qs,
            'card_state_filter': card_state_filter,
            'due_decks': due_decks,
            'total_due_cards': total_due_cards,
            'cards_by_state': cards_by_state,
        }
        return render(request, self.template_name, context)

class NotificationMarkAsReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        auth_user = request.user
        username = getattr(auth_user, 'username', None)
        email = getattr(auth_user, 'email', None)

        user_q = Q()
        if username:
            user_q |= Q(user__username=username)
        if email:
            user_q |= Q(user__email=email)

        queryset = Notification.objects.filter(user_q) if user_q else Notification.objects.none()
        notification = get_object_or_404(queryset, pk=pk)
        notification.status = True
        notification.save()

        return redirect(reverse('notification_list'))