from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "core"
urlpatterns = [
    path('', views.Home.as_view(),name='home'),
]
