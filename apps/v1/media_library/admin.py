from django.contrib import admin

# Register your models here.
from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'created_by']


# admin.site.register(Image, ImageAdmin)
