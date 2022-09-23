import os
import pytest
import json
from urllib.request import urlopen
from django.core.management import call_command
from django.db.models import Max
from episodes.models import Episode
from dotenv import load_dotenv


load_dotenv()


api_key = os.getenv('API_KEY')


@pytest.fixture
def omdb_season():
    response_series = urlopen(f'https://www.omdbapi.com/?i=tt2442560&apikey={api_key}')
    series = json.loads(response_series.read())
    seasons_count = int(series['totalSeasons'])
    return seasons_count


@pytest.mark.django_db
def test_importepisodes(omdb_season):
    call_command('importepisodes')
    season = Episode.objects.aggregate(Max('season'))['season__max']
    assert season == omdb_season, 'Wrong number of seasons downloaded'


@pytest.mark.django_db
def test_importepisodes_missing_season(omdb_season):
    call_command('importepisodes')
    Episode.objects.filter(season=omdb_season).delete()
    call_command('importepisodes')
    season = Episode.objects.aggregate(Max('season'))['season__max']
    assert season == omdb_season, 'Missing season is not downloaded'


@pytest.mark.django_db
def test_importepisodes_missing_season_episodes(omdb_season):
    call_command('importepisodes')
    Episode.objects.filter(season=omdb_season).delete()
    last_two_episodes = Episode.objects.filter(season=omdb_season-1).order_by('-number_episode').values('pk')[:2]
    Episode.objects.filter(pk__in=last_two_episodes).delete()
    call_command('importepisodes')
    season = Episode.objects.aggregate(Max('season'))['season__max']
    assert season == omdb_season, 'Missing episodes are not downloaded'
