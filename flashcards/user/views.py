
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.decorators import method_decorator


from .forms import UserForm, CreateUserForm, ChangeEmailForm
from folder.models import Folder
from .procedures import insert_user_user, loginUser, update_user_email,verify_user_password


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
        next_url = request.POST.get('next') or request.GET.get('next')  # <-- read the next parameter

        # user = authenticate(request, username=username, password=password)
        #
        # if user is not None:
        #     login(request, user)
        #     return redirect('home')   # home page
        # else:
        #     messages.error(request, "Username or password is incorrect")
        #     return redirect('login')

        #for this to work u need to create loginUser in ur mysql which can be found on the stored_procedure dir
        if loginUser(username, password):
            # request.session['username'] = username
            #need this for user to be authenticated using Django so that we can go to next views
            #because we are using LoginRequiredMixin
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # optionally create a Django user if it doesn't exist
                user = User.objects.create_user(username=username, password=password)
            login(request, user)  # <-- attaches user to session
            return redirect(next_url or 'home')
        else:
            #message = "Invalid username or password"
            messages.error(request, "Invalid username or password")

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

def logout_user(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('login')


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            auth_user = form.save()

            insert_user_user(auth_user.id) #get id cause it is in the stored procedure
            # redirect to login page with username password already in the inputs
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            login_url = f"{reverse('login')}?username={username}&password={password}"
            return redirect(login_url)

    context = {'form': form}
    return render(request, 'user/register.html', context)



# PROFILE Management
class ProfileView(LoginRequiredMixin,View):
    login_url = 'login'
    template_name = 'user/profile.html'
    def get(self, request):
        user =request.user

        context = {
            'username': user.username,
            'email': user.email,
            'created_at': user.date_joined,
        }
        return render(request, self.template_name,context)

class ChangeEmailView(LoginRequiredMixin,View):
    login_url = 'login'
    template_name = 'user/change_email.html'

    def get(self,request):
        # email = User.objects.get(username=request.session['username'])
        # form = UserForm(instance=email)
        user = request.user
        initial_data = {'email': user.email}
        form = ChangeEmailForm(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        # email = User.objects.get(username=request.session['username'])
        # form = UserForm(request.POST, instance=email)

        user = request.user
        form = ChangeEmailForm(request.POST)
        current_password = request.POST.get('current_password')
        error_password = None  # placeholder for password errors

        if not current_password or not verify_user_password(user.username, current_password):
            error_password = "Current password is incorrect"
            return render(request, self.template_name, {'form': form, 'error_password': error_password})

        if form.is_valid():
            new_email = form.cleaned_data.get('email')
            user.email = new_email
            user.save()

            update_user_email(user.username, new_email)
            messages.success(request,"Email successfully updated")
            return redirect('profile')


        return render(request, self.template_name,{'form': form,})


class ChangePasswordView(LoginRequiredMixin,View):
    login_url =  'login'
    template_name = 'user/change_password.html'

    def get(self, request):
        return render(request, self.template_name)


#LoginRequiredMixin does not allow user to go to that page without being logged in
class HomePageView(LoginRequiredMixin,View):
    login_url = 'login'
    template_name = 'user/home.html'

    def get(self, request):
        folders = Folder.objects.all()
        return render(request, self.template_name, {'folders': folders})

