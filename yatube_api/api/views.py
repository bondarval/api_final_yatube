from rest_framework import filters, viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Follow, Group, Post

from .mixins import ListRetrieveViewSet, ListCreateViewSet
from .permissions import AuthorOrReadOnly
from .serializers import CommentSerializer, FollowSerializer
from .serializers import GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Управление отображением публикаций(постов)"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ListRetrieveViewSet):
    """Управление отображением групп или сообществ"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]


class CommentViewSet(viewsets.ModelViewSet):
    """Управление отображением комментариев"""
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorOrReadOnly
    ]

    def get_queryset(self):
        post = Post.objects.get(id=self.kwargs['post_id'])
        return post.comments.all()

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(ListCreateViewSet):
    """Управление отображением подписок"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
