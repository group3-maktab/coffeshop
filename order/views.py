from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Sum, F
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from foodmenu.models import Food
from tables.models import Table
from utils import Cart, staff_or_superuser_required, StaffSuperuserRequiredMixin
from .forms import CartAddProductForm, OrderCreateForm, GetPhoneOrder
from order.models import OrderItem, Order


# Create your views here.


class CreateCartView(View):
    @staff_or_superuser_required
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Food, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     override_quantity=cd['override'])
        messages.success(request, 'Item added successfully!')
        return redirect('order:detail-cart')


class DeleteCartView(View):
    @staff_or_superuser_required
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Food, id=product_id)
        cart.remove(product)
        messages.success(request, 'Order deleted successfully!')
        return redirect('order:detail-cart')


class DetailCartView(View):
    template_name = 'Order_DetailCart.html'

    @staff_or_superuser_required
    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity': item['quantity'],
                'override': True})
        return render(request, self.template_name, {'cart': cart})


class MakeOrderView(View):
    template_name = 'Order_CreateOrder.html'

    @staff_or_superuser_required
    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        return render(request, self.template_name, {'cart': cart, 'form': form})

    @staff_or_superuser_required
    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():

            table = form.cleaned_data.get('table')
            table = Table.objects.get(pk=table.pk)

            if table.status == "F":
                messages.error(request, 'table is full!')
                return render(request, self.template_name, {'cart': cart, 'form': form})
            if table.status != "T":
                table.status = 'F'
                table.save()

            order = form.save()
            for item in cart:
                # print(order,item['product'],item['price'],item['quantity'])
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            messages.success(request, 'Order created successfully!')
            return render(request, self.template_name, {'order': order})
        else:
            messages.error(request, 'Invalid Data!')
            return render(request, self.template_name, {'cart': cart, 'form': form})


class ChangeOrderView(View):
    def post(self, request, pk):
        cart = Cart(request)
        cart.edit_orders(pk)
        messages.success(request, 'Order now is ready to change!')
        return redirect('order:detail-cart')


class BaseOrderListView(StaffSuperuserRequiredMixin, ListView):
    model = Order
    template_name = 'Order_ListOrder.html'
    context_object_name = 'orders'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        raise NotImplementedError("Subclasses must implement get_queryset method.")


class OrderWaitingListView(BaseOrderListView):
    def get_queryset(self):
        return Order.objects.filter(status='W')


class OrderFinishedListView(BaseOrderListView):
    def get_queryset(self):
        return Order.objects.filter(status='F')


class OrderPreparationListView(BaseOrderListView):
    def get_queryset(self):
        return Order.objects.filter(status='P')


class OrderTransmissionListView(BaseOrderListView):
    def get_queryset(self):
        return Order.objects.filter(status='T')


class OrderCanceldListView(BaseOrderListView):
    def get_queryset(self):
        return Order.objects.filter(status='C')


class ChangeStatusOrderView(StaffSuperuserRequiredMixin, View):
    def post(self, request, pk):
        new_status: str = request.POST.get('new_status')
        order = get_object_or_404(Order, id=pk)
        if new_status == 'F' and order.table.status != "T":
            table = Table.objects.get(pk=order.table.pk)
            table.status = 'E'
            table.save()
        order.status = new_status
        order.save()
        messages.success(request, 'Order changed successfully!')
        return redirect(f'order:list-order-{new_status.lower()}')


class ListOrderPhoneView(LoginRequiredMixin, View):
    template_name = 'Order_ListPhoneOrder.html'
    paginate_by = 10

    def get(self, request, phone):
        phone = str(phone)

        if request.user.is_superuser or request.user.is_staff:
            orders = Order.objects.filter(customer_phone=phone).select_related('table').order_by('-created_at')
        else:
            if not str(request.user.phone_number) == phone:
                messages.error(request, "You don't have permission to access others order.")
                orders = Order.objects.filter(customer_phone=request.user.phone_number).select_related('table').order_by('-created_at')
            else:
                orders = Order.objects.filter(customer_phone=request.user.phone_number).select_related('table').order_by('-created_at')

        paginator = Paginator(orders, self.paginate_by)
        page = request.GET.get('page')

        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'user_order': orders, 'phone': phone})


class OrderDetailView(LoginRequiredMixin, SingleObjectMixin, View):
    template_name = 'Order_DetailView.html'

    def get(self, request, pk):
        order = get_object_or_404(Order.objects.prefetch_related('items'), pk=pk)
        if not (request.user.is_superuser or request.user.is_staff) and order.customer_phone != str(
                request.user.phone_number):
            messages.error(request, "You don't have permission to access this order.")
            return redirect('order:phone-orders', request.user.phone_number)
        return render(request, self.template_name, {'order': order})




class GetPhoneOrderView(StaffSuperuserRequiredMixin, View):
    template_name = 'Order_GetPhoneOrder.html'
    form = GetPhoneOrder()

    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        form = GetPhoneOrder(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['customer_phone']
            return redirect('order:phone-orders', phone=phone_number)
        return render(request, self.template_name, {'form': form})


class CustomerOrdersView(StaffSuperuserRequiredMixin, View):
    template_name = 'Order_ListCustomer.html'
    paginate_by = 10
    def get(self, request):
        orders = Order.objects.filter(
            status='F'
        )
        customers_data = (
            orders
            .values('customer_phone')
            .annotate(count=Count('id'),
                      total = Sum(
                    F('items__price') * F('items__quantity'),
            )
                      )
            .order_by('-total')
        )

        paginator = Paginator(customers_data, self.paginate_by)
        page = request.GET.get('page')

        try:
            customers_data = paginator.page(page)
        except PageNotAnInteger:
            customers_data = paginator.page(1)
        except EmptyPage:
            customers_data = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'customer_orders': customers_data})