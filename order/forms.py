from django import forms
from django.core.validators import RegexValidator
from django.forms import inlineformset_factory
from .models import Order, OrderItem
from foodmenu.models import Food, Category

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={'class': 'btn btn-tertiary'})
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class OrderCreateForm(forms.ModelForm):

    customer_phone = forms.CharField(
        label='Phone Number',
        widget=forms.TextInput(attrs={'id': 'phone_number', 'class': 'form-control', 'placeholder': 'Phone'}),
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message='Phone number must be in the format 09XXXXXXXXX.',
                code='invalid_phone_number'
            )
        ]
    )

    class Meta:
        model = Order
        fields = ['customer_phone', 'table']
        widgets = {
            'table': forms.Select(attrs={'class': 'btn btn-info'},),
        }


class GetPhoneOrder(forms.Form):
    customer_phone = forms.CharField(
        label='Phone Number',
        widget=forms.TextInput(attrs={'id': 'phone_number', 'class': 'form-control', 'placeholder': 'Phone'}),
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message='Phone number must be in the format 09XXXXXXXXX.',
                code='invalid_phone_number'
            )
        ]
    )