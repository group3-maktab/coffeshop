from django.urls import path, include
from . import views

app_name = 'tables'
urlpatterns = [
    path('reservation', views.Reservation.as_view(), name='reservation'),
    path('reservation-list', views.ReservationList.as_view(), name='reservation-list'),
    path('reservation/<uuid:pk>', views.ReservationDetail.as_view(), name='reservation-detail'),
    path('reservation-get', views.ReservationGet.as_view(), name='reservation-get')

]
