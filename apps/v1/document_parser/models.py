from django.db import models

from ..core.abstract_models import AbstractDocument


# Create your models here.
class Document(AbstractDocument, models.Model):
    KING_COUNTY = 'KING COUNTY'
    DOCUMENT_FORMAT_TYPE_CHOICES = (
        (KING_COUNTY, KING_COUNTY),
    )
    document_format_type = models.CharField(choices=DOCUMENT_FORMAT_TYPE_CHOICES, default=KING_COUNTY, max_length=255)
