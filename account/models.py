from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
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
    def has_perm(self, obj=None):
        return self.is_superuser
    @staticmethod
    def generate_activation_code():
        from django.utils.crypto import get_random_string
        code = get_random_string(8)
        return code
    def set_activation_code(self):
        code = self.generate_activation_code()
        if UserProfile.objects.filter(activation_code=code).exists():
            self.set_activation_code()
        else:
            self.activation_code = code
            self.save()
    def send_activation_mail(self):
        message = f'Hello! Thank you for registering on our site! Your activation code: {self.activation_code}'
        send_mail(
            'Account verification',
            message,
            "test@gmail.com",
            [self.email]
        )

    def send_new_password(self, new_password):
        message = f'Your new password: {new_password}'
        send_mail(
            'Reset password',
            message,
            'test@gmail.com',
            [self.email]
        )
