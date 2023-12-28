from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from foodmenu.models import Food
from tables.models import Table
from utils import Cart, staff_or_superuser_required
from .forms import CartAddProductForm, OrderCreateForm
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
        return redirect('foods:list-food')


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
            messages.error(request, 'invalid data!')
            return render(request, self.template_name, {'cart': cart, 'form': form})


class ChangeOrderView(View):

    def post(self, request, pk):
        cart = Cart(request)
        cart.edit_orders(request, pk)
        messages.success(request, 'Order now is ready to change!')
        return redirect('order:detail-cart')


class OrderWaitingListView(ListView):
    model = Order
    template_name = 'Order_ListOrder.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(status='W')


class OrderFinishedistView(ListView):
    model = Order
    template_name = 'Order_ListOrder.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(status='F')


class OrderPreparationListView(ListView):
    model = Order
    template_name = 'Order_ListOrder.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(status='P')


class OrderTransmissionListView(ListView):
    model = Order
    template_name = 'Order_ListOrder.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(status='T')


class ChangeStatusOrderView(View):
    def post(self,request, pk):
        new_status:str = request.POST.get('new_status')
        order = get_object_or_404(Order, id=pk)
        if new_status == 'F':
            table = Table.objects.get(pk = order.table.pk)
            table.status = 'E'
            table.save()
        order.status = new_status
        order.save()
        messages.success(request, 'Order changed successfully!')
        return redirect(f'order:list-order-{new_status.lower()}')


