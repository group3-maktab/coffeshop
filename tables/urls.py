from django.urls import path, include
from . import views

app_name = 'tables'
urlpatterns = [
    path('create-reservation', views.CreateReservationView.as_view(), name='create-reservation'),
    path('list-reservation', views.ListReservationView.as_view(), name='list-reservation'),
    path('reservation/<uuid:pk>', views.DetailReservationView.as_view(), name='detail-reservation'),
    path('get-reservation', views.GetReservationView.as_view(), name='get-reservation'),
    path('create-table', views.CreateTableView.as_view(), name='create-table'),
    path('list-table', views.ListTableView.as_view(), name='list-table')
]
