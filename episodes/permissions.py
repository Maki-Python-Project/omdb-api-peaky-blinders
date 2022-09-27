from rest_framework import permissions
from rest_framework.response import Response
from django.db.models.query import QuerySet
from typing import Any


class AdminOrAccountOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request: Response, view: Any, obj: QuerySet) -> bool:
        return obj.customer == request.user or request.user.is_superuser
