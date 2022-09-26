import os
import json

from urllib.request import urlopen
from django.core.management.base import BaseCommand, CommandError
from episodes.serializers import EpisodeSerializer, ActorsSerializer, GenreSerializer
from episodes.models import Actor, Episode, Genre
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv('API_KEY')


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        response_series = urlopen(f'https://www.omdbapi.com/?i=tt2442560&apikey={api_key}')
        series = json.loads(response_series.read())
        seasons_count = int(series['totalSeasons'])

        language = series['Language']
        actors = []

        for name_surname in series['Actors'].split(', '):
            name_surname = name_surname.split()
            actors.append({
                'name': name_surname[0],
                'surname': name_surname[1],
            })

        if not Actor.objects.exists():
            actors_serializer = ActorsSerializer(data=actors, many=True)
            if actors_serializer.is_valid():
                actors_serializer.save()

        genres = []

        for genre in series['Genre'].split(', '):
            genres.append({
                'name': genre,
            })

        if not Genre.objects.exists():
            genres_serializer = GenreSerializer(data=genres, many=True)
            if genres_serializer.is_valid():
                genres_serializer.save()

        if not Episode.objects.exists():
            for i in range(1, seasons_count + 1):
                response_season = urlopen(
                    f'https://www.omdbapi.com/?t=Peaky%20Blinders&Season={i}&type=series&apikey={api_key}'
                )
                season = json.loads(response_season.read())
                episodes = season['Episodes']
                self.import_season(
                    i,
                    episodes,
                    genres,
                    actors,
                    language
                )
        else:
            local_episode = Episode.objects.order_by('-season', '-number_episode')[0]
            response_season = urlopen(
                f'https://www.omdbapi.com/?t=Peaky%20Blinders&Season={local_episode.season}&type=series&apikey={api_key}'
            )
            season = json.loads(response_season.read())
            episodes = season['Episodes']

            if (local_episode.season == seasons_count and
                    local_episode.number_episode < int(season['Episodes'][-1]['Episode'])):
                Episode.objects.filter(season=seasons_count).delete()
                self.import_season(
                    local_episode.season,
                    episodes,
                    int(local_episode.number_episode),
                    int(season['Episodes'][-1]['Episode']),
                    genres,
                    actors,
                    language
                    )
            elif local_episode.season < seasons_count:
                Episode.objects.filter(season=local_episode.season).delete()
                self.import_season(
                    local_episode.season,
                    episodes,
                    int(local_episode.number_episode),
                    int(season['Episodes'][-1]['Episode']),
                    genres,
                    actors,
                    language
                )
                for i in range(local_episode.season, seasons_count + 1):
                    Episode.objects.filter(season=i).delete()
                for i in range(local_episode.season + 1, seasons_count + 1):
                    response_season = urlopen(
                        f'https://www.omdbapi.com/?t=Peaky%20Blinders&Season={i}&type=series&apikey={api_key}'
                    )
                    season = json.loads(response_season.read())
                    episodes = season['Episodes']
                    self.import_season(i, episodes, genres, actors, language)

    def import_season(self, season, episodes, genres, actors,
                      language='English, Romanian, Irish Gaelic, Italian, Yiddish, French'):
        for episode in episodes:
            episode_data = {
                'title_episode': episode['Title'],
                'season': season,
                'released': episode['Released'],
                'number_episode': episode['Episode'],
                'imdb_rating': episode['imdbRating'],
                'genre': genres,
                'actors': actors,
                'language': language
            }

            episode_serializer = EpisodeSerializer(data=episode_data)

            if episode_serializer.is_valid():
                episode_serializer.save()
            else:
                raise CommandError(episode_serializer.errors)
