from django.urls import path, include

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.LandingPageView.as_view(),name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('profile/settings/change-email/', views.ChangeEmailView.as_view(), name='change_email'),
    path('profile/settings/change-password/', views.ChangePasswordView.as_view(), name='change_password'),


    path('home/', views.HomePageView.as_view(),name='home'),
    path('register/', views.registerPage, name='register'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('forgot-password/code', views.ForgotPasswordCodeView.as_view(), name='forgot_password_code'),
    path('forgot-password/changing-password', views.ForgotPasswordChangePasswordView.as_view(), name='forgot_password_changepw'),
    path('forgot-password/success', views.ForgotPasswordSuccessView.as_view(), name='forgot_password_success'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="user/forgot_password.html", success_url='/reset_password_sent/'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "user/forgot_password_code.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.ForgotPasswordChangePasswordView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/forgot_password_success.html'), name='password_reset_complete'),

    path("folder/", include("folder.urls")),
]
