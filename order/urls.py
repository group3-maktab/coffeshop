from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('', views.DetailCartView.as_view(), name='detail-cart'),
    path('add/<int:product_id>', views.CreateCartView.as_view(), name='create-cart'),
    path('delete/<int:product_id>', views.DeleteCartView.as_view(), name='delete-cart'),
    path('create/', views.MakeOrderView.as_view(), name='create-order'),
    path('orders/w', views.OrderWaitingListView.as_view(), name='list-order-w'),
    path('orders/p', views.OrderPreparationListView.as_view(), name='list-order-p'),
    path('orders/t', views.OrderTransmissionListView.as_view(), name='list-order-t'),
    path('orders/f', views.OrderFinishedistView.as_view(), name='list-order-f'),
    path('orders/change-status/<uuid:pk>', views.ChangeStatusOrderView.as_view(), name='change-status'),
]
