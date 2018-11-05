# Create your views here.
import os

from django.conf import settings
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
        wanted_docs = documents[:3]
        final_docs = []
        for doc in wanted_docs:
            try:
                # Check if file exist and it not exist delete object as well
                if not os.path.isfile(doc.file.path):
                    doc.delete()
                else:
                    final_docs.append(doc)
            except:
                print('Some Error')

        ctx['documents'] = final_docs
        return ctx


class HelpPageView(TemplateView):
    template_name = 'pages/help.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["email"] = settings.TESTING_EMAIL
        ctx["password"] = settings.TESTING_PASSWORD
        return ctx
