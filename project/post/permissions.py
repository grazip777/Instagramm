"""
устанавка ограничений на удаление и редактирование (только создатель),
но при этом читать пост могут все.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True # разрешение на чтение всем

        return obj.author == request.user # разрешение на редактирование или удаление
                                          # только автору
