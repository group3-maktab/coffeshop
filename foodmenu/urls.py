from django.urls import path, include
from . import views

app_name = 'foods'
urlpatterns = [
    path('list-food', views.ListFoodView.as_view(), name='list-food'),
    # path('create-food', views.CreateFoodView.as_view(), name='create-food'),
    path('create-category', views.CreateCategoryView.as_view(), name='create-category'),
    # path('unavailable-food', views.ListFoodView.as_view(), name='unavailable-food'),
    # path('unavailable-category', views.ListFoodView.as_view(), name='unavailable-category'),

]
