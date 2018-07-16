from django.forms import ModelForm

from apps.v1.document_parser.models import Document


class DocumentUploadForm(ModelForm):
    class Meta:
        fields = ['file']
        model = Document
