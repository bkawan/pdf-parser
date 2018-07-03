# Create your views here.
from django.views.generic import TemplateView

from ..document_parser.models import Document


class LandingPageView(TemplateView):
    template_name = 'pages/landing_page.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        documents = Document.objects.all()
        ctx['documents'] = documents

        return ctx
