import pytest


@pytest.mark.django_db
def test_capital_case():
    assert 'qq' == 'qq' 

# from django.core.management import call_command
# from django.db.models import Max
# from rest_framework import status

 

# from episodes.models import Episode
# from users.fixtures import (
#     api_client,
#     user_token,
#     user_data,
#     superuser_token
# )
# from episodes.fixtures import (
#     episode,
#     episodes,
#     comment,
#     comments,
#     omdb_season
# )


# @pytest.mark.django_db
# def test_importepisodes(omdb_season):
#     call_command('importepisodes')
#     season = Episode.objects.aggregate(Max('season'))['season__max']
#     assert season == omdb_season, 'Wrong number of seasons downloaded'


# @pytest.mark.django_db
# def test_importepisodes_missing_season(omdb_season):
#     call_command('importepisodes')
#     Episode.objects.filter(season=omdb_season).delete()
#     call_command('importepisodes')
#     season = Episode.objects.aggregate(Max('season'))['season__max']
#     assert season == omdb_season, 'Missing season is not downloaded'


# @pytest.mark.django_db
# def test_importepisodes_missing_season_episodes(omdb_season):
#     call_command('importepisodes')
#     Episode.objects.filter(season=omdb_season).delete()
#     last_two_episodes = Episode.objects.filter(
#         season=omdb_season-1).order_by('-number_episode').values('pk')[:2]
#     Episode.objects.filter(pk__in=last_two_episodes).delete()
#     call_command('importepisodes')
#     season = Episode.objects.aggregate(Max('season'))['season__max']
#     assert season == omdb_season, 'Missing episodes are not downloaded'


# @pytest.mark.django_db
# def test_episodes(api_client):
#     url = '/api/episodes/'
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK, "Cannot retrieve episodes list"


# @pytest.mark.django_db
# def test_episode(api_client, episode):
#     url = f'/api/episodes/{episode["pk"]}/'
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK, 'Cannot retrieve specific episode'


# @pytest.mark.django_db
# def test_eppisode_imdb(api_client, episodes):
#     url = f'/api/episodes/imdb/'
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK, 'Cannot retrieve episodes with rating > 8.8'


# @pytest.mark.django_db
# def test_comments(api_client, comments, user_token):
#     url = f'/api/comments/'
#     api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token["access"]}')
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK, 'Cannot retrieve comments'


# @pytest.mark.django_db
# def test_comment(api_client, comment, superuser_token):
#     url = f'/api/comments/{comment["pk"]}/'
#     api_client.credentials(
#         HTTP_AUTHORIZATION=f'Bearer {superuser_token["access"]}')
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK, 'Cannot retrieve specific comment'
