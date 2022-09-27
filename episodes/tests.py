import json
import numbers
import pytest
from urllib.request import urlopen
from django.core.management import call_command
from django.db.models import Max
from users.fixtures import (
    api_client,
    user_token,
    user_data,
    superuser_token
)
from episodes.models import Episode, Comment
from users.models import User
from rest_framework import status
from .fixtures import (
    episode,
    episodes,
    comment,
    comments,
    omdb_season
)


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
    last_two_episodes = Episode.objects.filter(
        season=omdb_season-1).order_by('-number_episode').values('pk')[:2]
    Episode.objects.filter(pk__in=last_two_episodes).delete()
    call_command('importepisodes')
    season = Episode.objects.aggregate(Max('season'))['season__max']
    assert season == omdb_season, 'Missing episodes are not downloaded'


@pytest.mark.django_db
def test_episodes(api_client, episodes):
    url = '/api/episodes/'
    response = api_client.get(url)
    for result in response.data['results']:
        assert Episode.objects.filter(
            season=result['season'],
            number_episode=result['number_episode']
        ).exists(), "Can't find episode with given data"
    assert response.status_code == status.HTTP_200_OK, "Cannot retrieve episodes list"


@pytest.mark.django_db
def test_episode(api_client, episode):
    url = f'/api/episodes/{episode["pk"]}/'
    response = api_client.get(url)
    assert Episode.objects.filter(
        season=response.data['season'],
        number_episode=response.data['number_episode']
    ), "Can't find episode with given data"
    assert response.status_code == status.HTTP_200_OK, 'Cannot retrieve specific episode'


@pytest.mark.django_db
def test_eppisode_imdb(api_client, episodes):
    url = f'/api/episodes/imdb/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, 'Cannot retrieve episodes with rating > 8.8'


@pytest.mark.django_db
def test_comments(api_client, comments, user_token):
    url = f'/api/comments/'
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token["access"]}')
    response = api_client.get(url)
    print(response.data)
    for result in response.data:
        print(result)
        assert Comment.objects.filter(
            text=result['text'],
            customer=User.objects.get(username=result['customer']).pk
        ).exists(), "Can't find comment with given data"
    assert response.status_code == status.HTTP_200_OK, 'Cannot retrieve comments'


@pytest.mark.django_db
def test_comment(api_client, comment, superuser_token):
    url = f'/api/comments/{comment["pk"]}/'
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {superuser_token["access"]}')
    response = api_client.get(url)
    assert Comment.objects.filter(
        text=response.data['text'],
        customer=User.objects.get(username=response.data['customer']).pk
    ).exists(), "Can't find comment with given data"
    assert response.status_code == status.HTTP_200_OK, 'Cannot retrieve specific comment'
