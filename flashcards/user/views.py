from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import UserForm,CreateUserForm
from folder.models import Folder
from django.db import transaction

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


#@login_required(login_url='login')
class HomePageView(View):
    template_name = 'user/home.html'

    def get(self, request):
        return render(request, self.template_name)

class HomePageView(View):
    template_name = 'user/home.html'

    def get(self, request):
        # show all folders regardless of user
        folders = Folder.objects.all()
        return render(request, self.template_name, {'folders': folders})

def logout_user(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('login')


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            #puts the data into the user_user aswell
            form.save()
            # redirect to login page with username password already in the inputs
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            login_url = f"{reverse('login')}?username={username}&password={password}"
            return redirect(login_url)

    context = {'form': form}
    return render(request, 'user/register.html', context)


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


