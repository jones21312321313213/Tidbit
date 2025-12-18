from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification

class NotificationListView(LoginRequiredMixin, View):
    template_name = 'notifications/notification_list.html'
    login_url = 'login'

    def get(self, request):
        # Now request.user is a proper 'User' instance, not a string
        user_notifications = Notification.objects.filter(user=request.user)
        
        filter_by = request.GET.get('filter', 'all')
        qs = user_notifications.order_by('-schedule')
        
        if filter_by == 'unread':
            qs = qs.filter(status=False)
        elif filter_by == 'read':
            qs = qs.filter(status=True)

        context = {
            'notifications': qs,
            'message': f'Viewing {filter_by} notifications',
            'filter': filter_by,
            'counts': {
                'all': user_notifications.count(),
                'unread': user_notifications.filter(status=False).count(),
                'read': user_notifications.filter(status=True).count(),
            }
        }
        return render(request, self.template_name, context)

class NotificationMarkAsReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # get_object_or_404 ensures the notification belongs to the logged-in user
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.status = True
        notification.save()

        next_filter = request.POST.get('filter', 'all')
        return redirect(f"{reverse('notification_list')}?filter={next_filter}")