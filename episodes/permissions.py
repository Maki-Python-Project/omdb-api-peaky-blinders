from rest_framework import permissions


class AdminOrAccountOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user or request.user.is_superuser
