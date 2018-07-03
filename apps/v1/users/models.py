from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.


from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(verbose_name='Email address', max_length=255, unique=True, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if not created and not hasattr(instance, 'auth_token'):
        Token.objects.create(user=instance)
    if created:
        Token.objects.create(user=instance)
