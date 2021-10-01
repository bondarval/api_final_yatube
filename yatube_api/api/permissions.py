from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, view, request, obj):
        return (
            request.action in (permissions.SAFE_METHODS, 'retrieve')
            or obj.author == view.user
               )
