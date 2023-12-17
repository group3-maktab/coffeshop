from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import Reservation as ReservationForm
from .forms import ReservationGetForm
from .models import Reservation as ReservationModel


class Reservation(View):
    template_name = 'reservation.html'
    def get(self,request):
        form = ReservationForm()
        return render(request,self.template_name,{'form' : form})
    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            datetime = form.cleaned_data['datetime']
            number_of_persons = form.cleaned_data['number_of_persons']
            reservation = ReservationModel(phone_number=phone_number,
                                           datetime=datetime,
                                           number_of_persons=number_of_persons)
            reservation.save()
            messages.success(request,
                    'Reservation created successfully.')
            return redirect('core:home')
        else:
            return render(request,self.template_name,{'form' : form})


class ReservationList(View):
    template_name = 'reservation_list.html'
    def get(self, request):
        reservationlist = ReservationModel.objects.all()
        return render(request,self.template_name,{'reservationlist' : reservationlist})

class ReservationDetail(View):
    template_name = 'reservation_detail.html'
    def get(self, request, pk):
        try:
            reservation = ReservationModel.objects.get(pk = pk)
            pk = reservation.pk
            phone_number = reservation.phone_number
            datetime = reservation.datetime
            number_of_persons = reservation.number_of_persons
            table = reservation.table
            status = reservation.status
            context = {'id': id, 'phone_number': phone_number, 'datetime': datetime,
                       'number_of_persons':number_of_persons,
                       'table': table, 'status':status}
        except ReservationModel.DoesNotExist:
            messages.error(request,
                             'Reservation does not exist.')
        return render(request, self.template_name, context=context)

def ReservationGet(View):
    template_name = 'reservation_get.html'
    def get (request):
        form = ReservationGetForm()
        return render(request, self.template_name, {'form': form})