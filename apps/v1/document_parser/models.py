from datetime import datetime, date

from django.db import models

from apps.v1.document_parser.king_county_pdf_parser import clean_king_county_pdf_file
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
        if not self.pk:
            if not self.name:
                self.name = self.file.name
        super().save(*args, **kwargs)
        if not self.document_created_at:
            file_path = self.file.path
            data = clean_king_county_pdf_file(file_path, pages=[0,1])
            case_status_date = data['case_status_date']
            if not len(case_status_date.split(".")) == 3:
                case_status_date += f'.{date.today().year}'
            datetime_object = datetime.strptime(case_status_date, '%m.%d.%Y')
            self.document_created_at = datetime_object
            self.save()
