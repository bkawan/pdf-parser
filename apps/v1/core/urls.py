from django.urls import path

from .views import LandingPageView, HelpPageView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('help/', HelpPageView.as_view(), name='help')
]
