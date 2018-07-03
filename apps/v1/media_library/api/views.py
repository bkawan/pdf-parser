from rest_framework.viewsets import ModelViewSet

from apps.v1.media_library.api.serializers import ImageSerializer
from ..models import Image


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    # permission_classes = []
    # authentication_classes = []

    def get_queryset(self):
        qs = self.queryset
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)
