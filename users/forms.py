from django import forms
from django.core.validators import RegexValidator

class SendSMSForm(forms.Form):
    phone_number = forms.CharField(
        label='Enter Phone Number:',
        widget=forms.TextInput(attrs={'id': 'phone_number'}),
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message='Phone number must be in the format 09XXXXXXXXX.',
                code='invalid_phone_number'
            )
        ]
    )



class VerifyOTPForm(forms.Form):
    otp = forms.CharField(
        label='Enter code:',
        widget=forms.TextInput(attrs={'id': 'otp'}),
        required=True
    )
