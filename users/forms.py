from django import forms
from django.core.validators import RegexValidator

class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


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
    verification_method = forms.ChoiceField(
        choices=[('phone', 'Phone Number'), ('email', 'Email')],
        initial='email',
        widget=forms.RadioSelect,
        label='Preferred Verification Method')


class VerifyOTPForm(forms.Form):
    otp = forms.CharField(
        label='Enter code:',
        widget=forms.TextInput(attrs={'id': 'otp'}),
        required=True)


class SetPasswordForm(forms.Form):
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, validators=[RegexValidator(regex=r'^.{5,}$', message='Password must be at least 5 characters long.')])
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2