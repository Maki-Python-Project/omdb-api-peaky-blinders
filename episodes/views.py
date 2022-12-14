from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models.query import QuerySet

from .models import Episode, Comment
from .serializers import EpisodeSerializer, CommentSerializer
from .filters import CommentFilter, ImdbFilter
from .permissions import AdminOrAccountOwnerPermission
from .pagination import StandardResultsSetPagination


class EpisodeList(generics.ListCreateAPIView):
    serializer_class = EpisodeSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
    ]
    filterset_fields = [
        'id', 'title_episode', 'number_episode', 'season', 'language'
    ]
    search_fields = ['title_episode', 'number_episode', 'season']
    ordering_fields = ['id', 'number_episode', 'season']

    def get_queryset(self) -> QuerySet[Episode]:
        return Episode.objects.all().prefetch_related('genre', 'actors')

    @method_decorator(cache_page(60*2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class EpisodeDetail(generics.RetrieveAPIView):
    queryset = Episode.objects.all().prefetch_related('genre', 'actors')
    serializer_class = EpisodeSerializer


class CommentList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all().select_related('customer')
    serializer_class = CommentSerializer
    filterset_class = CommentFilter

    def perform_create(self, serializer: CommentSerializer) -> None:
        serializer.save(
            customer=self.request.user
        )


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    filterset_class = CommentFilter
    serializer_class = CommentSerializer

    def get_permissions(self) -> permissions.BasePermission:
        if self.request.method not in permissions.SAFE_METHODS:
            return [AdminOrAccountOwnerPermission(), IsAuthenticated()]
        return [IsAuthenticated()]


class EpisodeImdb(generics.ListCreateAPIView):
    queryset = Episode.objects.filter(imdb_rating__gte=8.8)
    serializer_class = EpisodeSerializer
    filterset_class = ImdbFilter
