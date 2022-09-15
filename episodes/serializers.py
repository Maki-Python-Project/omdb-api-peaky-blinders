from rest_framework import serializers
from .models import Episode, Comment


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = [
            'id',
            'title_episode',
            'season',
            'released',
            'number_episode',
            'imdb_rating',
            'genre',
            'actor',
            'language'
        ]


class CommentSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'episode', 'customer', 'published']
