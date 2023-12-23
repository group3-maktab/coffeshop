from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('', views.DetailCartView.as_view(), name='detail-cart'),
    path('add/<int:product_id>', views.CreateCartView.as_view(), name='create-cart'),
    path('delete/<int:product_id>', views.DeleteCartView.as_view(), name='delete-cart'),
    path('create/', views.MakeOrderView.as_view(), name='create-order'),
]
