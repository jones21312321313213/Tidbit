from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Count, Q

from .models import Notification
from deck.models import Deck

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

        if user_q:
            user_notifications = Notification.objects.filter(user_q)
        else:
            user_notifications = Notification.objects.none()

        filter_by = request.GET.get('filter', 'all')
        qs = user_notifications.order_by('-schedule')

        if filter_by == 'unread':
            qs = qs.filter(status=False)
        elif filter_by == 'read':
            qs = qs.filter(status=True)

        # compute decks that have due cards for the current user (match by username/email)
        now = timezone.now()
        card_q = Q()
        if username:
            card_q |= Q(card__user__username=username)
        if email:
            card_q |= Q(card__user__email=email)

        if card_q:
            card_q = card_q & Q(card__next_review__lte=now)
            due_decks = Deck.objects.filter(user_q).annotate(
                due_count=Count('card', filter=card_q)
            ).filter(due_count__gt=0).order_by('-due_count')
        else:
            due_decks = []

        context = {
            'notifications': qs,
            'message': f'Viewing {filter_by} notifications',
            'filter': filter_by,
            'counts': {
                'all': user_notifications.count(),
                'unread': user_notifications.filter(status=False).count(),
                'read': user_notifications.filter(status=True).count(),
            },
            'due_decks': due_decks,
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

        next_filter = request.POST.get('filter', 'all')
        return redirect(f"{reverse('notification_list')}?filter={next_filter}")