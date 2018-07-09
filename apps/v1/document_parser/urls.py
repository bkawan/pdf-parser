from django.urls import path

from apps.v1.document_parser.views import download_csv

app_name = 'document_parser'
urlpatterns = [
    path('download/<slug:slug>/', download_csv, name='export_to_csv')
]
