from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.v1.document_parser.king_county_pdf_parser import clean_king_county_pdf_file
from ..models import Document


class KingCountyPdfParseAPIView(APIView):
    def get(self, request, format=None, **kwargs):
        """
        Return a list of all users.
        """
        document = get_object_or_404(Document, slug=kwargs.get('slug'))
        document_path = document.file.path
        data = clean_king_county_pdf_file(file_path=document_path)

        return Response({'data':data})
