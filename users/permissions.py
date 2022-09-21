from rest_framework import permissions


class AccountOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.username == request.user.username)
        return obj.username == request.user.username
