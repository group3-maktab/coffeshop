from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('set-password', views.SetPasswordView.as_view(), name='set-password'),
    path('chengepass', views.ForgotPassword.as_view(), name='forgot'),
    path('login_code', views.AuthCode.as_view(), name='login_code'),
    path('logout', views.LogOutView.as_view(), name="logout"),
    path('register', views.Register.as_view(), name="register"),
    path('verification', views.Verification.as_view(), name="verification"),
]
