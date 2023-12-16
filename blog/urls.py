from django.urls import path
from . import views

urlpatterns = [
    path('create_blog', views.CreateBlogRecord.as_view(), name='create_blog'),
    path('blogs_list', views.BlogsListView.as_view(), name='blog_list'),
    path('<slug:slug>', views.BlogDetailView.as_view(), name='blog_detail'),
    path('update_blog/<slug:slug>', views.UpdateBlogRecord.as_view(), name='update_blog'),
    path('delete_blog/<slug:slug>', views.DeleteBlogView.as_view(), name='delete_blog'),
]
app_name = 'blog'
