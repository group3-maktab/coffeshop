from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,AbstractUser ,Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from twilio.rest import Client
import random

# import os
# from dotenv import load_dotenv

# load_dotenv()

# secret_key = os.getenv('SECRET_KEY')


account_sid="AC7b880f6bcd7d76164b08b45c97e4693f"
auth_token="73b4c27d580e3f83775f99e691f2ca91"
twilio_phone_number="14846601335"


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='customuser_groups'  # Add a unique related_name
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_user_permissions'  # Add a unique related_name
    )
    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def send_otp(self):
        otp = self.generate_otp()
        self.otp = otp
        self.otp_expiry = timezone.now() + timezone.timedelta(minutes=5)
        self.save()

        # Use Twilio to send OTP via SMS
        
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f'Your code is: {otp}',
            from_=twilio_phone_number,
            to=self.phone_number
        )

    def check_otp(self, entered_otp):
        return self.otp == entered_otp and timezone.now() < self.otp_expiry
