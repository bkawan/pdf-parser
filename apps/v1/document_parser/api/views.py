import os

from django.utils import timezone
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.v1.core.api.permissions import IsSuperuserOrIsOwner
from apps.v1.document_parser.king_county_pdf_parser import clean_king_county_pdf_file
from ..models import Document


class KingCountyPdfParseAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperuserOrIsOwner]

    def get(self, request, format=None, **kwargs):
        """
        Return a list of all users.
        """
        document = get_object_or_404(Document, slug=kwargs.get('slug'))
        document_path = document.file.path
        if not os.path.isfile(document_path):
            raise NotFound(f"The request file not found or delete from the server located at {document.file}")

        data = clean_king_county_pdf_file(file_path=document_path)
        data['case_status_date'] = timezone.localtime(document.created_at).strftime('%m/%d/%Y')

        return Response({'data':data})
