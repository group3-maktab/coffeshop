from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'
urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('send_sms', views.SendOtpView.as_view(), name='send_sms'),
    path('login_code', views.Auth.as_view(), name='login_code'),
    path('auth_sms', views.VerifyOtpView.as_view(), name='auth_sms'),
    path('logout', views.LogOutView.as_view(), name="logout"),
]
