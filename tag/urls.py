from django.urls import path
from . import views

app_name = 'tags'
urlpatterns = [
    path('create-tag', views.CreateTagView.as_view(), name='create-tag'),
    path('', views.TagListView.as_view(), name='tag'),
]