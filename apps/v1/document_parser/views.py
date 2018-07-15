# Create your views here.

import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..document_parser.king_county_pdf_parser import clean_king_county_pdf_file
from ..document_parser.models import Document


@login_required
def download_csv(request, **kwargs):
    # Create the HttpResponse object with the appropriate CSV header.
    document = get_object_or_404(Document, slug=kwargs.get('slug'))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{document.name}.csv"'
    document_path = document.file.path
    data = clean_king_county_pdf_file(file_path=document_path)
    writer = csv.writer(response)
    writer.writerow(list(data['case_list'][0].keys()) + ['case_status_date'])
    data['case_status_date'] = document.document_created_at.strftime('%m/%d/%Y')
    rows = [list(d.values()) + [data['case_status_date']] for d in data['case_list']]
    for row in rows:
        writer.writerow(row)
    return response


class DocumentCreateView(LoginRequiredMixin, CreateView):
    fields = ['file']
    template_name = 'document_parser/document_upload.html'
    model = Document
    success_url = reverse_lazy('landing_page')
