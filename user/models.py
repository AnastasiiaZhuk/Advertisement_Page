from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from user.utilities import send_auth_messages

user_register = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_auth_messages(kwargs['instance'])
    user_register.connect(user_registrated_dispatcher)


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, verbose_name='Activated?')
    send_message = models.BooleanField(default=True, verbose_name='Send messages?')

    class Meta(AbstractUser.Meta):
        pass