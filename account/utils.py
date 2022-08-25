from django.core.mail import send_mail

from account.models import UserProfile


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

def send_new_password(new_pass, email):
    message = f'Your new password: {new_pass}'
    send_mail(
        'Reset password',
        message,
        'test@gmail.com',
        [email]
    )
