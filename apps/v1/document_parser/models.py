from django.db import models

from ..core.abstract_models import AbstractDocument, AbstractSlug


# Create your models here.
class Document(AbstractSlug, AbstractDocument, models.Model):
    KING_COUNTY = 'KING COUNTY'
    DOCUMENT_FORMAT_TYPE_CHOICES = (
        (KING_COUNTY, KING_COUNTY),
    )
    document_format_type = models.CharField(choices=DOCUMENT_FORMAT_TYPE_CHOICES, default=KING_COUNTY, max_length=255)
    document_created_at = models.DateTimeField(blank=True, null=True, help_text='Date of  document creation date')

    @property
    def slug_field(self):
        return self.file

    def save(self, *args, **kwargs):
        if not self.pk and not self.name or self.pk and not self.name:
            self.name = self.file.name
        super().save(*args, **kwargs)
