from django.urls import path

from .views import LandingPageView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page')
]
