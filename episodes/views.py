import imp
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Episode, Comment
from .serializers import EpisodeSerializer, CommentSerializer
from .filters import CommentFilter


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
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_class = CommentFilter

    def perform_create(self, serializer):
        serializer.save(
            customer=self.request.user
        )
