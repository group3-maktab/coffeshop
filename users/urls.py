from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'users'
urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('send_sms', views.SendOtpView.as_view(), name='send_sms'),
    path('login_code', views.Auth.as_view(), name='login_code'),
    path('auth_sms', views.VerifyOtpView.as_view(), name='auth_sms'),
    # path('logout', LogoutView.as_view(next_page='user:login'), name="logout"),
    # path('register', views.RegisterView.as_view(), name="register"),
]
