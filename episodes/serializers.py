from rest_framework import serializers
from .models import Episode


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
