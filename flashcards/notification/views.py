from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse

# Check your template path and correct this string if necessary!
# Example using 'user/notification_list.html' as previously discussed:
class NotificationListView(View):
    template_name = 'notifications/notification_list.html'

    def get(self, request):
        # In a real app, you would fetch the user's notifications here
        # For now, pass an empty list or mock data to avoid template errors
        context = {
            'notifications': [], # Ensure this key exists for the template loop
            'message': 'Viewing all notifications'
        }
        return render(request, self.template_name, context)


# View to mark a specific notification as read
class NotificationMarkAsReadView(View):
    def post(self, request, pk):

        # Logic to mark Notification with pk as read goes here
        print(f"Notification {pk} marked as read.")

        # Redirects back to the list using the URL name 'notification_list'
        return redirect('notification_list')

    # ... (rest of the class)