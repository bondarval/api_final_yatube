from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, view, request, obj):
        if request.action == 'list' or request.action == 'retrieve':
            return True
        return obj.author == view.user
