# forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone

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

    def clean_datetime(self):
        datetime = self.cleaned_data.get('datetime')

        if datetime:
            now = timezone.now()
            delta = datetime - now
            if delta.total_seconds() < 24 * 60 * 60:

                raise ValidationError('Datetime must be at least 24 hours from now.')

        return datetime

class ReservationGetForm(forms.Form):
    code = forms.UUIDField(label="label",widget=forms.TextInput(attrs={'class': 'form-control'}))

class CreateTableForm(forms.Form):
    number = forms.IntegerField(min_value=1,label="label", widget=forms.TextInput(attrs={'class': 'form-control'}))
