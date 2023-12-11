from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('blog/<slug:title>', views.BlogDetailView.as_view(), name='login'),
    path('blogs', views.BlogsListView.as_view(), name='login'),
    path('create_blog', views.CreateBlogRecord.as_view(), name='create_blog'),
    path('update_blog', views.UpdateBlogRecord.as_view(), name='edit_blog'),
    path('delete_blog', views.DeleteBlogRecord.as_view(), name='delete_blog'),
]
