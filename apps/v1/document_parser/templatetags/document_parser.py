from django import template

from apps.v1.document_parser.forms import DocumentUploadForm

register = template.Library()


@register.inclusion_tag('document_parser/templatetags/document_upload_form.html', takes_context=True)
def get_document_upload_form(context):
    data = {
        'form':DocumentUploadForm()
    }

    return data
