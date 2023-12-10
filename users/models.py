from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# Create your models here.

class UserModelManager(BaseUserManager):
    def create_user(self,phone,password = None,**kwargs):
        if phone :
            user = self.model(phone = phone, **kwargs)
            user.set_password(password)
            user.save(using=self._db)
            return user
        else:
            