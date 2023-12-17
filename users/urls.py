from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('login', views.UsersLoginView.as_view(), name='login'),
    path('set-password', views.UsersSetPasswordView.as_view(), name='set-password'),
    path('chengepass', views.UsersForgotPasswordView.as_view(), name='forgot'),
    path('login_code', views.UsersAuthCodeView.as_view(), name='login_code'),
    path('logout', views.UsersLogoutView.as_view(), name="logout"),
    path('register', views.UsersRegisterView.as_view(), name="register"),
    path('verification', views.UsersVerificationView.as_view(), name="verification"),
]
