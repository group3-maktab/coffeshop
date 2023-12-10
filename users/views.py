from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from .models import CustomUser
from django.contrib.auth import login
from django.urls import reverse


# Create your views here.

class Login(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)


class SendOtpView(View):
    def post(self, request):
        phone_number = request.POST.get('phone_number')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(phone_number=phone_number)

        otp, otp_expiry = user.send_otp()
        request.session['otp'] = otp
        request.session['otp_expiry'] = otp_expiry
        request.session['phone_number'] = phone_number
        return redirect(reverse('users:login_code'))


class Auth(View):
    template_name = 'auth_sms.html'

    def get(self, request):
        return render(request, self.template_name)


class VerifyOtpView(View):
    def post(self, request):
        entered_otp = request.POST.get('otp')
        phone_number = request.session.get('phone_number')
        otp = request.session.get('otp')
        otp_expiry = request.session.get('otp_expiry ')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.check_otp(otp,otp_expiry,entered_otp):
                login(request, user)  # :-/
                return redirect('core:home')
            else:
                return redirect('login', {'error': 'Invalid code'})
        except CustomUser.DoesNotExist:
            return redirect('login', {'error': 'User not found'})
