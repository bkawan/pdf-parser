# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models

from apps.v1.core.abstract_models import AbstractCreatedAtModifiedAt
from apps.v1.core.model_utils import image_upload_to

User = get_user_model()


class Image(AbstractCreatedAtModifiedAt, models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to=image_upload_to)
    image_alt = models.CharField(max_length=255, blank=True)
    image_credit = models.CharField(max_length=255, blank=True)
    image_credit_link = models.URLField(blank=True, null=True)
    caption = models.CharField(max_length=150, blank=True, null=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.image.url
