from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

class LandingPageView(View):
    template_name = 'user/index.html'

    def get(self,request):
        return render(request, self.template_name)

class LoginView(View):
    template_name = 'user/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')   # home page
        else:
            messages.error(request, "Username or password is incorrect")
            return redirect('login')


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
    template_name = 'user/profile.html'
    def get(self, request):
        return render(request, self.template_name)

class ChangeEmailView(View):
    template_name = 'user/change_email.html'

    def get(self,request):
        return render(request, self.template_name)

class ChangePasswordView(View):
    template_name = 'user/change_password.html'

    def get(self, request):
        return render(request, self.template_name)


class HomePageView(View):
    template_name = 'user/home.html'

    def get(self, request):
        return render(request, self.template_name)


def logout_user(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('login')

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


