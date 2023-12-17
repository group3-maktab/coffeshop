from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('create-blog', views.CreateBlogView.as_view(), name='create-blog'),
    path('list-blog', views.ListBlogView.as_view(), name='list-blog'),
    path('<slug:slug>', views.DetailBlogView.as_view(), name='detail-blog'),
    path('update-blog/<slug:slug>', views.UpdateBlogView.as_view(), name='update-blog'),
    path('delete-blog/<slug:slug>', views.DeleteBlogView.as_view(), name='delete-blog'),
]
