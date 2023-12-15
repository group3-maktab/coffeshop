from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'
urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    # path('cheng_password', views.Login.as_view(), name='chenge_password'),
    # path('forgot', views.Login.as_view(), name='forgot'),
    path('login_code', views.Auth_Phone.as_view(), name='login_code'),
    path('logout', views.LogOutView.as_view(), name="logout"),
    path('register', views.Register.as_view(), name="register"),
    path('verification', views.Verification.as_view(), name="verification"),
]
