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



class RegistrationForm(forms.Form):
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
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    verification_method = forms.ChoiceField(
        choices=[('phone', 'Phone Number'), ('email', 'Email')],
        initial='phone',
        widget=forms.RadioSelect,
        label='Preferred Verification Method')
    username = forms.CharField(label='Username', help_text='Enter your email or phone number for login.')


class VerifyOTPForm(forms.Form):
    otp = forms.CharField(
        label='Enter code:',
        widget=forms.TextInput(attrs={'id': 'otp'}),
        required=True)
