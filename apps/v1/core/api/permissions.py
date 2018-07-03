from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id


class IsSuperuserOrIsOwner(permissions.BasePermission):
    def __init__(self):
        self.request_user_unique_field = 'id'
        self.object_unique_field = 'id'

    def has_object_permission(self, request, view, obj):
        obj_permission = eval(f'request.user.{self.request_user_unique_field}') == eval(
            f'obj.{self.object_unique_field}')
        return obj_permission or request.user.is_superuser


class GenericIsOwnerOrIsSuperuser(permissions.BasePermission):
    """
    This class handles generic object level permission for all the models.
    It takes request user unique field and object's unique field
    """

    def __init__(self):
        self.request_user_unique_field = 'id'
        self.object_unique_field = 'id'

    def has_permission(self, request, view):
        obj_permission = eval("(f'request.user.{self.request_user_unique_field}' == f'obj.{self.object_unique_field}')")
        return obj_permission or request.user.is_superuser
