from django_filters import rest_framework as filters

from .models import Comment


class CommentFilter(filters.FilterSet):
    episode = filters.CharFilter(field_name='episode__title_episode', lookup_expr='iexact')
    author = filters.CharFilter(field_name='customer__username', lookup_expr='iexact')

    class Meta:
        model = Comment
        fields = ['id', 'episode', 'author']
