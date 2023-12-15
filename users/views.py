from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from .forms import VerifyOTPForm, RegistrationForm, SetPasswordForm, LoginForm
from .models import CustomUser
import dotenv

from .utils import Authentication
dotenv.load_dotenv()

# todo:DOCUMENTATION

class Login(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:home')
            else:
                messages.error(request, 'Auth faild')
                return redirect('users:login')
        else:
            messages.error(request, 'Invalid data')
            return redirect('users:login')






class Auth_Phone(View):
    template_name = 'login_code.html'

    def get(self, request):
        form = VerifyOTPForm()
        if request.user.is_authenticated:
            return redirect('core:home')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        entered_otp = request.POST.get('otp')
        phone_number = request.session.get('phone_number')
        email = request.session.get('email')
        otp = request.session.get('otp')
        otp_expiry = request.session.get('otp_expiry')
        otp_expiry = timezone.datetime.fromtimestamp(otp_expiry, tz=timezone.get_current_timezone())
        verification_method = request.session['v_m']
        if verification_method == 'phone' or verification_method == 'email' and Authentication.check_otp(otp, otp_expiry, entered_otp) :
                return redirect('users:set-password')
        else:
            messages.error(request, 'Invalid code')
        return redirect('users:login')



class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('core:home'))


# views.py

class Register(View):
    template_name = 'register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']

            verification_method = form.cleaned_data['verification_method']


            request.session['phone_number'] = phone_number
            request.session['email'] = email
            request.session['v_m'] = verification_method


            messages.success(request, f'Registration successful. Please verify your {verification_method} !')
            return redirect('users:verification')
        else:
            messages.error(request, 'Invalid registration form data.')

        return render(request, self.template_name, {'form': form})


class Verification(View):
    def get(self,request):
        phone_number = request.session['phone_number']
        email = request.session['email']
        verification_method = request.session['v_m']

        if verification_method == 'phone':
            otp, otp_expiry = Authentication.send_otp(phone_number)

            request.session['otp'] = otp
            request.session['otp_expiry'] = int(otp_expiry.timestamp())
            request.session['phone_number'] = phone_number
            messages.success(request, 'CODE sent successfully. Please check your phone.')
            return redirect('users:login_code')
        else:
            otp, otp_expiry = Authentication.send_otp_email(email)
            request.session['otp'] = otp
            request.session['otp_expiry'] = int(otp_expiry.timestamp())
            request.session['email'] = email
            messages.success(request, 'CODE sent successfully. Please check your email.')
            return redirect('users:login_code')


class SetPasswordView(View):
    template_name = 'set_password.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        else:
            form = SetPasswordForm()
            return render(request,self.template_name,{'form':form})


    def post(self, request):
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            phone_number = request.session.get('phone_number')
            email = request.session.get('email')
            verification_method = request.session.get('v_m')

            if not (phone_number and email and verification_method):
                messages.error(request, 'Invalid session data.')
                return redirect('users:register')


            user = CustomUser.objects.create_user(phone_number=phone_number, email=email,
                                                  password=form.cleaned_data['password2'])
            user.save()
            login(request, user)  # :-/
            messages.success(request, 'Account created successfully.')
            return redirect('core:home')
        else:
            messages.error(request, 'Invalid password.')

        return render(request, self.template_name, {'form': form})