from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.

class LandingPageView(View):
    template_name = 'user/index.html'

    def get(self,request):
        return render(request, self.template_name)

class LoginView(View):
    template_name = 'user/login.html'

    def get(self,request):
        return render(request, self.template_name)

class RegisterView(View):
    template_name = 'user/register.html'

    def get(self, request):
        return render(request, self.template_name)


class ForgotPasswordView(View):
    template_name = 'user/forgot_password.html'

    def get(self,request):
        return render(request, self.template_name)

class ForgotPasswordCodeView(View):
    template_name = 'user/forgot_password_code.html'

    def get(self,request):
        return render(request, self.template_name)

class ForgotPasswordChangePasswordView(View):
    template_name = 'user/forgot_password_changepw.html'

    def get(self,request):
        return render(request, self.template_name)

class ForgotPasswordSuccessView(View):
    template_name = 'user/forgot_password_success.html'

    def get(self,request):
        return render(request, self.template_name)

# PROFILE Management
class ProfileView(View):
    template_name = 'tomake'
    def get(self, request):
        return HttpResponse('Viewing profile')

class ChangeEmailView(View):
    template_name = 'todo'

    def get(self,request):
        return HttpResponse('Change email')

class ChangePasswordView(View):
    template_name = 'todo'

    def get(self, request):
        return HttpResponse('Change password')

class ChangeUsernameView(View):
    template_name = 'todo'

    def get(self, request):
        return HttpResponse('Change username')

class HomePageView(View):
    template_name = 'user/home.html'

    def get(self, request):
        return render(request, self.template_name)


#Dont know if these below are part of user functionalities can remove
#Notification
# Gibalhin nakos notif - jm was here
# class NotificationView(View):
#     template_name = 'todo'
#
#     def get(self, request):
#         return HttpResponse('Viewing notification')
#

#Deck
# class DeckCreateView(View):
#     template_name = 'todo'

#     def get(self, request):
#         return HttpResponse('creating deck')

#Card


