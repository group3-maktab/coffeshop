from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

import dotenv


dotenv.load_dotenv()


class UserManager(BaseUserManager):

    def create_user(self, phone_number, email, password=None, **extra_fields):
        if not phone_number and not email:
            raise ValueError('The phone number or email field must be set')
        user = self.model(phone_number=phone_number, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
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
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True, verbose_name='last')
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    """django.core.management.base.SystemCheckError: SystemCheckError: System check identified some issues: ERRORS: 
    auth.User.groups: (fields.E304) Reverse accessor 'Group.user_set' for 'auth.User.groups' clashes with reverse 
    accessor for 'users.User.groups'. HINT: Add or change a related_name argument to the definition for 
    'auth.User.groups' or 'users.User.groups'. auth.User.user_permissions: (fields.E304) Reverse accessor 
    'Permission.user_set' for 'auth.User.user_permissions' clashes with reverse accessor for 
    'users.User.user_permissions'. HINT: Add or change a related_name argument to the definition for 
    'auth.User.user_permissions' or 'users.User.user_permissions'. users.User.groups: (fields.E304) 
    Reverse accessor 'Group.user_set' for 'users.User.groups' clashes with reverse accessor for 
    'auth.User.groups'. HINT: Add or change a related_name argument to the definition for 'users.User.groups' 
    or 'auth.User.groups'. users.User.user_permissions: (fields.E304) Reverse accessor 'Permission.user_set' 
    for 'users.User.user_permissions' clashes with reverse accessor for 'auth.User.user_permissions'. HINT: Add 
    or change a related_name argument to the definition for 'users.User.user_permissions' or 
    'auth.User.user_permissions'.
        
        
####### for this bug we should make these groups and permissions attr and make custom related_name:
    """
    # groups = models.ManyToManyField(
    #     Group,
    #     verbose_name=_('groups'),
    #     blank=True,
    #     related_name='users_groups')
    #
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name=_('user permissions'),
    #     blank=True,
    #     related_name='user_perms')
