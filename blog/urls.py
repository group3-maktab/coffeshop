from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('<slug:slug>/',views.BlogDetailView.as_view(), name='blog_detail'),
    path('blogs', views.BlogsListView.as_view(), name='blog_list'),
    path('create_blog', views.CreateBlogRecord.as_view(), name='create_blog'),
    path('update_blog', views.UpdateBlogRecord.as_view(), name='edit_blog'),
    # path('delete_blog', views.DeleteBlogRecord.as_view(), name='delete_blog'),
]
