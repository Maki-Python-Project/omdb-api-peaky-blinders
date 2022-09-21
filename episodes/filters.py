from django_filters import rest_framework as filters

from .models import Comment, Episode


class CommentFilter(filters.FilterSet):
    episode = filters.CharFilter(field_name='episode__title_episode', lookup_expr='iexact')
    author = filters.CharFilter(field_name='customer__username', lookup_expr='iexact')

    class Meta:
        model = Comment
        fields = ['id', 'episode', 'author']


class ImdbFilter(filters.FilterSet):
    season = filters.NumberFilter(field_name='season', lookup_expr='exact')

    class Meta:
        model = Episode
        fields = ['season']
