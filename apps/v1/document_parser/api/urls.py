from django.urls import path

from . import views

urlpatterns = [
    path('document/<slug:slug>/', views.KingCountyPdfParseAPIView.as_view())
]
