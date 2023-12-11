from django.contrib.auth.backends import ModelBackend
from .models import CustomUser


class PhoneBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, otp=None, **kwargs):
        try:
            user = CustomUser.objects.get()
        except CustomUser.DoesNotExist:
            return None

        if user.check_otp(otp):
            return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get()
        except CustomUser.DoesNotExist:
            return None
