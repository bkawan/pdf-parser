from django.contrib import admin
# Register your models here.
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(admin.ModelAdmin):
    exclude = ('groups', 'user_permissions')


# admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
