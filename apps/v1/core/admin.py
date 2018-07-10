from django.contrib import admin

# Register your models here.
from rest_framework.authtoken.models import Token

admin.site.unregister(Token)