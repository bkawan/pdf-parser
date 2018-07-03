# class UserViewSet(ReadOnlyModelViewSet):
from django.contrib.auth.models import update_last_login
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.v1.core.api.permissions import IsSuperuserOrIsOwner
from .serializers import UserSerializer, UserSignupSerializer
from ..models import User


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        update_last_login(None, user)
        user_data = UserSerializer(user, many=False).data
        return Response(user_data)


class UserSignupView(CreateAPIView):
    serializer_class = UserSignupSerializer
    queryset = User.objects.all()
    permission_classes = []


class RetrieveUpdateModelMixin(mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               GenericViewSet):
    pass


class UserViewSet(RetrieveUpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperuserOrIsOwner]
