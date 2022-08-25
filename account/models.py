from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserManager(BaseUserManager):
    def _create(self, email, password, **kwargs):
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_active', False)
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self._create(email, password, **kwargs)

class UserProfile(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField('Telephone number', max_length=16)
    name = models.CharField('User name', max_length=50)
    last_name = models.CharField('User last name', max_length=50)

    is_active = models.BooleanField('Active', default=False)
    is_staff = models.BooleanField('Admin', default=False)
    is_superuser = models.BooleanField('Superuser', default=False)

    activation_code = models.CharField(max_length=8, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    def has_module_perms(self, app_label):
        return self.is_staff
    def has_perm(self, obj):
        return self.is_superuser

