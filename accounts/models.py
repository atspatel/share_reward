from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator, URLValidator

import uuid


class UserManager(BaseUserManager):
    def create_user(self, phone, first_name, password=None, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('Please Enter Phone number')

        user_obj = self.model(phone=phone,
                              first_name=first_name,
                              is_active=is_active,
                              is_admin=is_admin)
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, phone, first_name, password=None):
        user = self.create_user(
            phone, first_name, password=password, is_admin=True)
        return user


class AbstractTimeClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creation_time = models.DateTimeField(default=timezone.now, blank=True)
    creation_time.editable = True
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, AbstractTimeClass):
    phone = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=100)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def name(self):
        return self.first_name


class UserOTPTable(AbstractTimeClass):
    phone = models.CharField(max_length=15)
    otp = models.IntegerField()

    REQUIRED_FIELDS = ['phone', 'otp']
