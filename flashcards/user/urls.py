from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingPageView.as_view(),name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/settings/change-email/', views.ChangeEmailView.as_view(), name='logout'),
    path('profile/settings/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('profile/settings/change-username/', views.ChangeUsernameView.as_view(), name='change_password')

]
