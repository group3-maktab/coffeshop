from django.urls import path, include
from . import views

app_name = 'foods'
urlpatterns = [
    path('list-food', views.ListFoodView.as_view(), name='list-food'),
    path('create-food', views.CreateFoodView.as_view(), name='create-food'),
    path('update-food/<int:pk>', views.UpdateFoodView.as_view(), name='update-food'),
    path('update-category/<int:pk>', views.UpdateCategoryView.as_view(), name='update-category'),
    path('delete-food/<int:pk>', views.DeleteFoodView.as_view(), name='delete-food'),
    path('delete-category/<int:pk>', views.DeleteCategoryView.as_view(), name='delete-category'),
    path('create-category', views.CreateCategoryView.as_view(), name='create-category'),
    # path('unavailable-food', views.ListFoodView.as_view(), name='unavailable-food'),
    # path('unavailable-category', views.ListFoodView.as_view(), name='unavailable-category'),

]
