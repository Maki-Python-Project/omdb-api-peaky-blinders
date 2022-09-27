import os
import json

from urllib.request import urlopen
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from dotenv import load_dotenv

from episodes.serializers import EpisodeSerializer, ActorsSerializer, GenreSerializer
from episodes.models import Actor, Episode, Genre


load_dotenv()

api_key = os.getenv('API_KEY')


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        response_series = urlopen(f'https://www.omdbapi.com/?i=tt2442560&apikey={api_key}')
        series = json.loads(response_series.read())
        seasons_count = int(series['totalSeasons'])
        if not Episode.objects.exists():
            for i in range(1, seasons_count + 1):
                self.import_season(i)
        else:
            local_episode = Episode.objects.order_by('-season', '-number_episode')[0]
            response_season = urlopen(
                f'https://www.omdbapi.com/?t=Peaky%20Blinders&Season={local_episode.season}&type=series&apikey={api_key}'
            )
            season = json.loads(response_season.read())

            if (local_episode.season == seasons_count and
                    local_episode.number_episode < int(season['Episodes'][-1]['Episode'])):
                Episode.objects.filter(season=seasons_count).delete()
                self.import_season(local_episode.season)
            elif local_episode.season < seasons_count:
                Episode.objects.filter(season=local_episode.season).delete()
                self.import_season(local_episode.season)
                for i in range(local_episode.season, seasons_count + 1):
                    Episode.objects.filter(season=i).delete()
                    response_season = urlopen(f'https://www.omdbapi.com/?t=Peaky%20Blinders&Season={i}&type=series&apikey={api_key}')
                    season = json.loads(response_season.read())
                    self.import_season(i)

    def import_season(self, season_number):
        response_season = urlopen(
            f'https://www.omdbapi.com/?t=Peaky%20Blinders&Season={season_number}&type=series&apikey={api_key}'
        )
        season = json.loads(response_season.read())
        episodes = season['Episodes']
        for episode in episodes:
            self.import_episode(episode['imdbID'])

    def import_episode(self, id):
        response_episode = urlopen(f'https://www.omdbapi.com/?i={id}&apikey={api_key}')
        episode = json.loads(response_episode.read())

        actors = []
        for name_surname in episode['Actors'].split(', '):
            name_surname = name_surname.split()
            actor = {
                'name': name_surname[0],
                'surname': name_surname[1],
            }
            if not Actor.objects.filter(name=actor['name'], surname=actor['surname']).exists():
                actors_serializer = ActorsSerializer(data=actor)
                if actors_serializer.is_valid():
                    actors_serializer.save()
            actors.append(actor)

        genres = []
        for genre in episode['Genre'].split(', '):
            genre = {
                'name': genre,
            }
            if not Genre.objects.filter(name=genre['name']).exists():
                genres_serializer = GenreSerializer(data=genre)
                if genres_serializer.is_valid():
                    genres_serializer.save()
            genres.append(genre)
    
        episode_data = {
            'title_episode': episode['Title'],
            'season': int(episode['Season']),
            'released': datetime.strptime(episode['Released'], '%d %b %Y').date(),
            'number_episode': episode['Episode'],
            'imdb_rating': float(episode['imdbRating']),
            'genre': genres,
            'actors': actors,
            'language': episode['Language']
        }

        episode_serializer = EpisodeSerializer(data=episode_data)
        if episode_serializer.is_valid():
            episode_serializer.save()
        else:
            raise CommandError(episode_serializer.errors)
