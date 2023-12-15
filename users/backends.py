from django.contrib.auth.backends import ModelBackend
from .models import CustomUser


class PhoneBackend(ModelBackend):
    class CustomUserBackend(ModelBackend):
        def authenticate(self, request, phone_number=None, password=None, **kwargs):
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                return None

            if user.check_password(password):
                return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
