from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from .forms import SendSMSForm, VerifyOTPForm
from .models import CustomUser
import dotenv

dotenv.load_dotenv()


# todo:DOCUMENTATION

class Login(View):
    template_name = 'login.html'

    def get(self, request):
        form = SendSMSForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        phone_number = request.POST.get('phone_number')

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(phone_number=phone_number)

        otp, otp_expiry = user.send_otp()

        request.session['otp'] = otp
        request.session['otp_expiry'] = int(otp_expiry.timestamp())
        request.session['phone_number'] = phone_number

        messages.success(request, 'OTP sent successfully. Please check your phone.')

        return redirect('users:login_code')


class Auth(View):
    template_name = 'login_code.html'

    def get(self, request):
        form = VerifyOTPForm()
        if request.user.is_authenticated:
            return redirect('core:home')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        entered_otp = request.POST.get('otp')
        phone_number = request.session.get('phone_number')
        otp = request.session.get('otp')
        otp_expiry = request.session.get('otp_expiry')
        # otp_expiry = timezone.datetime.fromtimestamp(otp_expiry) {{can't compare offset-naive and offset-aware
            # datetimes}}
        otp_expiry = timezone.datetime.fromtimestamp(otp_expiry, tz=timezone.get_current_timezone())

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.check_otp(otp, otp_expiry, entered_otp):
                login(request, user)  # :-/
                return redirect('core:home')
            else:
                messages.error(request, 'Invalid code')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found')

        return redirect('users:login')


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('core:home'))
