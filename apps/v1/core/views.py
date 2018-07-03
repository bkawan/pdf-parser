# Create your views here.
from django.views.generic import TemplateView


class LandingPageView(TemplateView):
    template_name = 'pages/landing_page.html'
