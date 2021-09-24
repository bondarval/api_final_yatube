from rest_framework import filters
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Follow, Group, Post

from .mixins import BaseViewSet, FollowingViewSet
from .permissions import ReadOrAuthorOnly, ReadOnly
from .serializers import CommentSerializer, FollowSerializer
from .serializers import GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Управление отображением публикаций(постов)"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ReadOrAuthorOnly
    ]
    authentication_classes = (JWTAuthentication,)
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(BaseViewSet):
    """Управление отображением групп или сообществ"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    authentication_classes = (JWTAuthentication,)


class CommentViewSet(viewsets.ModelViewSet):
    """Управление отображением комментариев"""
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ReadOrAuthorOnly
    ]
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post.comments.all()

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(FollowingViewSet):
    """Управление отображением подписок"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (JWTAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
