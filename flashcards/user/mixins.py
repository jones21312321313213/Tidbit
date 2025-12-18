from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

#THIS FILE IS PARA DILI MAKA ACCESS ANG MGA USER NA DILI LOGGED IN ON SECURED ENDPOINTS
class LoginRequiredMessageMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                request,
                "You must log in to continue."
            )
        return super().dispatch(request, *args, **kwargs)
