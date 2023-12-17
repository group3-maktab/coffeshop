from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import NoReverseMatch
from django.views import View
from .forms import Reservation as ReservationForm
from .forms import ReservationGetForm
from .models import Reservation as ReservationModel
from .models import Table


class Reservation(View):
    template_name = 'reservation.html'

    def get(self, request):
        form = ReservationForm()
        return render(request, self.template_name, {'form': form})

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
            return render(request, self.template_name, {'form': form})


class ReservationList(View):
    template_name = 'reservation_list.html'

    def get(self, request):
        reservationlist = ReservationModel.objects.all()
        tables = Table.objects.all()
        return render(request, self.template_name, {'reservationlist': reservationlist, 'tables': tables})

    def post(self, request):
        reservation_id = request.POST.get('reservation_id')
        action = request.POST.get('action')

        try:
            reservation = ReservationModel.objects.get(id=reservation_id)

            if action == 'set':
                table_id = request.POST.get('table_id')
                if table_id == 'Null':
                    reservation.table = None
                    reservation.save()
                else:
                    table = Table.objects.get(id=table_id)
                    reservation.table = table
                    reservation.save()
                messages.success(request, 'Table set successfully.')

                new_status = request.POST.get('new_status')
                reservation.status = new_status
                reservation.save()
                messages.success(request, 'Status updated successfully.')
            return redirect('tables:reservation-list')

        except ReservationModel.DoesNotExist:
            messages.error(request, 'Reservation does not exist.')


class ReservationDetail(View):
    template_name = 'reservation_detail.html'

    def get(self, request, pk):
        tables = Table.objects.all()
        try:
            reservation = ReservationModel.objects.get(pk=pk)
            pk = reservation.pk
            phone_number = reservation.phone_number
            datetime = reservation.datetime
            number_of_persons = reservation.number_of_persons
            table = reservation.table
            status = reservation.status
            context = {'id': id, 'phone_number': phone_number, 'datetime': datetime,
                       'number_of_persons': number_of_persons,
                       'table': table, 'status': status,
                       'tables': tables, 'pk': pk}
        except ReservationModel.DoesNotExist:
            messages.error(request,
                           'Reservation does not exist.')
        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        reservation_id = request.POST.get('reservation_id')
        action = request.POST.get('action')

        try:
            reservation = ReservationModel.objects.get(id=reservation_id)

            if action == 'set':
                table_id = request.POST.get('table_id')
                if table_id == 'Null':
                    reservation.table = None
                    reservation.save()
                else:
                    table = Table.objects.get(id=table_id)
                    reservation.table = table
                    reservation.save()
                messages.success(request, 'Table set successfully.')
                new_status = request.POST.get('new_status')
                reservation.status = new_status
                reservation.save()
                messages.success(request, 'Status updated successfully.')
            return redirect('tables:reservation-detail', pk)

        except ReservationModel.DoesNotExist:
            messages.error(request, 'Reservation does not exist.')


class ReservationGet(View):
    template_name = 'reservation_get.html'

    def get(self, request):
        form = ReservationGetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ReservationGetForm(request.POST)
        try:
            if form.is_valid():
                return redirect('tables:reservation-detail', form.cleaned_data['code'])
            else:
                messages.error(request,
                               'Reservation does not exist.')
                return render(request, self.template_name, {'form': form})
        except NoReverseMatch:
            messages.error(request,
                           'Invalid code')
            return render(request, self.template_name, {'form': form})
