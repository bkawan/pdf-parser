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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from .api import urls as api_urls

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_SITE_INDEX_TITLE
urlpatterns = [
                  path('accounts/login/', auth_views.login, {'template_name':'core/login.html'}, name='login'),
                  path('accounts/logout/', auth_views.logout, {'template_name':'core/logout.html'}, name='logout'),
                  path(settings.DJANGO_ADMIN_URL, admin.site.urls),
                  path('document-parser/', include('apps.v1.document_parser.urls')),
                  path('', include('apps.v1.core.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += api_urls.urlpatterns
urlpatterns += api_urls.urlpatterns
