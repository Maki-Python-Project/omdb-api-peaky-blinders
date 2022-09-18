from rest_framework import serializers
from .models import Episode, Comment, Genre, Actor


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'name',
        ]


class ActorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = [
            'name',
            'surname',
        ]


class EpisodeSerializer(serializers.ModelSerializer):
    genres = serializers.ReadOnlyField()
    actors = serializers.ReadOnlyField()

    class Meta:
        model = Episode
        fields = [
            'title_episode',
            'season',
            'released',
            'number_episode',
            'imdb_rating',
            'genres',
            'actors',
            'language'
        ]


class CommentSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'episode', 'customer', 'published']
