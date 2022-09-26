from typing import Type
from rest_framework import serializers
from collections import OrderedDict

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
    genre = GenreSerializer(many=True)
    actors = ActorsSerializer(many=True)

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
            'actors',
            'language'
        ]

    def create(self, validated_data: OrderedDict) -> Type[Episode]:
        genres = validated_data.pop('genre')
        actors = validated_data.pop('actors')
        episode = Episode.objects.create(**validated_data)
        genre_objects = []
        for genre in genres:
            genre_objects.append(Genre.objects.get(name=genre['name']).pk)
        episode.genre.set(genre_objects)
        actor_objects = []
        for actor in actors:
            actor_objects.append(Actor.objects.get(name=actor['name'], surname=actor['surname']).pk)
        episode.actors.set(actor_objects)
        return episode


class CommentSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'episode',
            'customer',
            'published'
        ]
