# Create your views here.
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..document_parser.models import Document


class LandingPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/landing_page.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        documents = Document.objects.all().order_by('-created_at')
        total_documents = Document.objects.count()
        if total_documents > 3:
            unwanted_docs = documents[3:]
            for doc in unwanted_docs:
                try:
                    if os.path.isfile(doc.file.path):
                        os.remove(doc.file.path)
                except:
                    print('Some error')
                doc.delete()
        ctx['documents'] = documents
        return ctx
