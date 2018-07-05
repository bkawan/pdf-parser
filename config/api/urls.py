"""lpcore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from apps.v1.users.api.views import CustomObtainAuthToken, UserSignupView

urlpatterns = [
    path('api/v1/users/', include('apps.v1.users.api.urls')),
    path('api/v1/auth/login/', CustomObtainAuthToken.as_view()),
    path('api/v1/auth/signup/', UserSignupView.as_view()),
    path('api/v1/media-library/', include('apps.v1.media_library.api.urls')),
    path('api/v1/document-parser/', include('apps.v1.document_parser.api.urls')),

]

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='ALL API URLS')

urlpatterns += [
    path('apis', schema_view)
]
