from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Episode, Comment
from .serializers import EpisodeSerializer, CommentSerializer
from .filters import CommentFilter
from .permissions import AdminOrAccountOwnerPermission


class EpisodeList(generics.ListCreateAPIView):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    filter_backends = [
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
    ]
    filterset_fields = [
        'id', 'title_episode', 'number_episode', 'season', 'language'
    ]
    search_fields = ['title_episode', 'number_episode', 'season']
    ordering_fields = ['id', 'number_episode', 'season']


class EpisodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer


class CommentList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_class = CommentFilter

    def perform_create(self, serializer: CommentSerializer) -> None:
        serializer.save(
            customer=self.request.user
        )


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self) -> permissions.BasePermission:
        if self.request.method not in permissions.SAFE_METHODS:
            return [AdminOrAccountOwnerPermission(), IsAuthenticated()]
        return [IsAuthenticated()]
