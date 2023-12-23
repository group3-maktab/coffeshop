from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views import View

from foodmenu.models import Category
from order.forms import OrderItemForm, OrderForm
from order.models import Order, OrderItem


# Create your views here.





