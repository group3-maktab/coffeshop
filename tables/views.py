from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import NoReverseMatch
from django.views import View

from order.models import Order
from utils import staff_or_superuser_required
from .forms import Reservation as ReservationForm
from .forms import ReservationGetForm, CreateTableForm
from .models import Reservation as ReservationModel
from .models import Table
from django.views.generic import ListView

class CreateReservationView(View):
    template_name = 'Reservation_CreateTemplate.html'

    @staff_or_superuser_required
    def get(self, request):
        form = ReservationForm()
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
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


class ListReservationView(LoginRequiredMixin, View):
    template_name = 'Reservation_ListTemplate.html'

    @staff_or_superuser_required
    def get(self, request):
        reservationlist = ReservationModel.objects.all()
        tables = Table.objects.all()
        return render(request, self.template_name, {'reservationlist': reservationlist, 'tables': tables})

    @staff_or_superuser_required
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
            return redirect('tables:list-reservation')

        except ReservationModel.DoesNotExist:
            messages.error(request, 'Reservation does not exist.')


class DetailReservationView(View):
    template_name = 'Reservation_DetailTemplate.html'

    @staff_or_superuser_required
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

    @staff_or_superuser_required
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
            return redirect('tables:detail-reservation', pk)

        except ReservationModel.DoesNotExist:
            messages.error(request, 'Reservation does not exist.')


class GetReservationView(View):
    template_name = 'Reservation_GetTemplate.html'

    @staff_or_superuser_required
    def get(self, request):
        form = ReservationGetForm()
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
    def post(self, request):
        form = ReservationGetForm(request.POST)
        try:
            if form.is_valid():
                return redirect('tables:detail-reservation', form.cleaned_data['code'])
            else:
                messages.error(request,
                               'Reservation does not exist.')
                return render(request, self.template_name, {'form': form})
        except NoReverseMatch:
            messages.error(request,
                           'Invalid code')
            return render(request, self.template_name, {'form': form})

class CreateTableView(View):
    template_name = 'Reservation_CreateTable.html'

    @staff_or_superuser_required
    def get(self,request):
        form = CreateTableForm()
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
    def post(self,request):
        form = CreateTableForm(request.POST)
        if form.is_valid():
            Table.objects.all().delete()
            for i in range(1,form.cleaned_data['number'] +1):
                Table.objects.create(number=i)
            messages.success(request,
                           'Tables created successfully')

            redirect('tables:list-table')

#todo @staff_or_superuser_required
class ListTableView(ListView):
    model = Table
    template_name = 'Reservation_ListTableTemplate.html'
    context_object_name = 'table'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_orders'] = {}
        for table_instance in context['table']:
            try:
                order = Order.objects.filter(table=table_instance, status__in=["W", "P", "T"]).first()
                # print(context['table_orders'][table_instance.id],table_instance.id,"\n\n\n")
                context['table_orders'][table_instance.id] = order
            except Order.DoesNotExist:
                pass
        return context


class ChangeStatusTableView(View):

    @staff_or_superuser_required
    def post(self,request,pk,status):
        table = Table.objects.get(pk=pk)
        table.status = status
        table.save()
        messages.success(request, 'Table status changed successfully!')
        return redirect('tables:list-table')