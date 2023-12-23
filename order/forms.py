from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem
from foodmenu.models import Food, Category

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_phone', 'table']