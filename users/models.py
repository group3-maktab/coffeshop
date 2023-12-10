from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
from twilio.rest import Client
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import random
import dotenv
import os

dotenv.load_dotenv()


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
    """
    django mixins:Mixins are not meant to stand alone; instead, they are designed to be mixed into other classes to
    extend or enhance their functionality. PermissionsMixin:provides a set of fields and methods for handling
    permissions related to authentication and authorization in a Django model. AbstractBaseUser: This class is
    suitable when you want more control over the fields and behavior of your user model and are willing to define
    those details yourself. AbstractUser: is suitable for projects where the default set of user fields and methods
    are sufficient or require minimal customization.
    """
    phone_number = models.CharField(max_length=11, unique=True, validators=[
        RegexValidator(
            regex=r'^09\d{9}$',
            message='Phone number must start with "09" and have 11 digits.',
            code='invalid_phone_number'
        )])
    # otp = models.CharField(max_length=6, null=True, blank=True)
    # otp_expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    """django.core.management.base.SystemCheckError: SystemCheckError: System check identified some issues: ERRORS: 
    auth.User.groups: (fields.E304) Reverse accessor 'Group.user_set' for 'auth.User.groups' clashes with reverse 
    accessor for 'users.CustomUser.groups'. HINT: Add or change a related_name argument to the definition for 
    'auth.User.groups' or 'users.CustomUser.groups'. auth.User.user_permissions: (fields.E304) Reverse accessor 
    'Permission.user_set' for 'auth.User.user_permissions' clashes with reverse accessor for 
    'users.CustomUser.user_permissions'. HINT: Add or change a related_name argument to the definition for 
    'auth.User.user_permissions' or 'users.CustomUser.user_permissions'. users.CustomUser.groups: (fields.E304) 
    Reverse accessor 'Group.user_set' for 'users.CustomUser.groups' clashes with reverse accessor for 
    'auth.User.groups'. HINT: Add or change a related_name argument to the definition for 'users.CustomUser.groups' 
    or 'auth.User.groups'. users.CustomUser.user_permissions: (fields.E304) Reverse accessor 'Permission.user_set' 
    for 'users.CustomUser.user_permissions' clashes with reverse accessor for 'auth.User.user_permissions'. HINT: Add 
    or change a related_name argument to the definition for 'users.CustomUser.user_permissions' or 
    'auth.User.user_permissions'.
        
        
####### for this bug we should make these groups and permissions attr and make custom related_name:
    """
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='users_groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='user_perms'
    )

    def send_otp(self):
        otp = self.generate_otp()
        # self.otp = otp
        # self.otp_expiry = timezone.now() + timezone.timedelta(minutes=5)
        otp_expiry = timezone.now() + timezone.timedelta(minutes=5)
        self.save()

        # todo: dotenv# #done
        account_sid = os.getenv('account_sid')
        auth_token = os.getenv('auth_token')
        twilio_phone_number = os.getenv('twilio_phone_number')

        dist_phone_number = self.phone_number.replace("0", "+98", 1)

        client = Client(account_sid, auth_token)
        print("Phone Number:", self.phone_number)
        message = client.messages.create(
            body=f'Your code is: {otp}',
            from_=twilio_phone_number,
            to=dist_phone_number
        )

        print("Twilio Response:", message)
        return otp, otp_expiry

    @staticmethod
    def check_otp(otp, otp_expiry, entered_otp):
        return otp == entered_otp and timezone.now() < otp_expiry
