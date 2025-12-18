
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetConfirmView

from .forms import UserForm, CreateUserForm, ChangeEmailForm
from .procedures import insert_user_user, loginUser, update_user_email,verify_user_password,update_userPassword,get_userInfo
from .mixins import LoginRequiredMessageMixin


from folder.models import Folder
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

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')   # home page
        else:
            messages.error(request, "Username or password is incorrect")
            return redirect('login')

        #for this to work u need to create loginUser in ur mysql which can be found on the stored_procedure dir
        # if loginUser(username, password):
        #     # request.session['username'] = username
        #     #need this for user to be authenticated using Django so that we can go to next views
        #     #because we are using LoginRequiredMixin
        #
        #
        #     user = User.objects.get(username=username)
        #     login(request, user)  # <-- attaches user to session
        #     return redirect(next_url or 'home')
        # else:
        #     #message = "Invalid username or password"
        #     messages.error(request, "Invalid username or password")

        return render(request, self.template_name)

class ForgotPasswordView(View):
    template_name = 'user/forgot_password.html'

    def get(self,request):
        return render(request, self.template_name)

class ForgotPasswordCodeView(View):
    template_name = 'user/forgot_password_code.html'

    def get(self,request):
        return render(request, self.template_name)

class ForgotPasswordChangePasswordView(PasswordResetConfirmView):
    template_name = 'user/forgot_password_changepw.html'
    success_url = "/forgot-password/success"

    def form_valid(self, form):
        response = super().form_valid(form)

        # user whose password was just reset
        username = self.user.username

        update_userPassword(username)

        return response

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
            login_url = f"{reverse('login')}?username={username}&password={password}" #para auto butang user & pass sa input fields sa login page
            return redirect(login_url)

    context = {'form': form}
    return render(request, 'user/register.html', context)



# PROFILE Management
class ProfileView(LoginRequiredMessageMixin,View):
    login_url = 'login'
    template_name = 'user/profile.html'
    def get(self, request):

        user = get_userInfo(request.user.username)

        context = {
            'userId': user["userId"],
            'username': user["username"],
            'email': user["email"],
            'created_at': user["created_at"],
        }
        return render(request, self.template_name,context)

class ChangeEmailView(LoginRequiredMessageMixin,View):
    login_url = 'login'
    template_name = 'user/change_email.html'


    def get(self,request):
        # email = User.objects.get(username=request.session['username'])
        # form = UserForm(instance=email)
        user = request.user
        initial_data = {'email': user.email}
        form = ChangeEmailForm(initial=initial_data)

        context = {
            'form': form,
            'userId': get_userInfo(user.username)["userId"],
        }

        return render(request, self.template_name, context)

    def post(self,request):
        # email = User.objects.get(username=request.session['username'])
        # form = UserForm(request.POST, instance=email)

        user = request.user
        form = ChangeEmailForm(request.POST)
        current_password = request.POST.get('current_password')


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


class ChangePasswordView(LoginRequiredMessageMixin, View):
    login_url = 'login'
    template_name = 'user/change_password.html'

    def get(self, request):
        form = PasswordChangeForm(request.user)
        context = {
            'form': form,
            'userId': get_userInfo(request.user.username)["userId"],
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()  # updates auth_user.password
            update_session_auth_hash(request, user)

            update_userPassword(user.username) #gets the updated password from auth_user table and put its in user_user tbl

            messages.success(request, "Password successfully updated")
            return redirect('profile')

        messages.error(request, "Please fix the errors below")
        return render(request, self.template_name, {'form': form})


#LoginRequiredMixin does not allow user to go to that page without being logged in
class HomePageView(LoginRequiredMessageMixin,View):
    login_url = 'login'
    template_name = 'user/home.html'

    def get(self, request):
        folders = Folder.objects.all()
        return render(request, self.template_name, {'folders': folders})

