<<<<<<< HEAD
# notifications/views.py
=======
>>>>>>> main
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse


class NotificationListView(View):
    template_name = 'notifications/notification_list.html'

    def get(self, request):
        return render(request, self.template_name, {'message': 'Viewing all notifications'})


# View to mark a specific notification as read
class NotificationMarkAsReadView(View):
    def post(self, request, pk):

<<<<<<< HEAD
        # For now, just a dummy response
=======
        # For now dummy response
>>>>>>> main
        print(f"Notification {pk} marked as read.")

        # Typically redirects back to the notification list or another page
        return redirect('notification_list')

    def get(self, request, pk):
        # For testing/simplicity, you might allow GET, but POST is better practice for state change
        return HttpResponse(f'Marking notification {pk} as read')
