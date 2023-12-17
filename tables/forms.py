# forms.py
from django import forms
from django.core.validators import RegexValidator


class Reservation(forms.Form):
    phone_number = forms.CharField(
        label='Phone Number',
        widget=forms.TextInput(attrs={'id': 'phone_number'}),
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message='Phone number must be in the format 09XXXXXXXXX.',
                code='invalid_phone_number'
            )
        ]
    )
    datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',),)
    number_of_persons = forms.IntegerField(min_value=1)

class ReservationGetForm(forms.Form):
    code = forms.UUIDField()