from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from foodmenu.models import Food
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

            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
        messages.success(request, 'Order created successfully!')
        return render(request, self.template_name, {'order': order})


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


class ChangeStatusView(View):
    def post(self,request, pk):
        new_status = request.POST.get('new_status')
        order = get_object_or_404(Order, id=pk)
        order.status = new_status
        order.save()
        return redirect('order:list-order-w')