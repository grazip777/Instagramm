"""
setting restrictions on deletion and editing (only the creator),
But at the same time, everyone can read the post.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True # Permission to read to all

        return obj.author == request.user # Permission to edit or delete
                                          # Only the author
