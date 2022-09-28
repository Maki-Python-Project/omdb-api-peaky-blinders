import os
import json
import pytest

from datetime import date
from urllib.request import urlopen
from dotenv import load_dotenv

from episodes.models import Episode, Genre, Actor, Comment
from users.models import User


load_dotenv()


api_key = os.getenv('API_KEY')


@pytest.fixture
def episode(db):
    actor_data = {
        'name': 'Name',
        'surname': 'Actor'
    }
    actors = Actor(**actor_data)
    actors.save()
    genre_data = {
        'name': 'Genre'
    }
    genre = Genre(**genre_data)
    genre.save()
    episode_data = {
        'pk': 1,
        'title_serials': 'Title',
        'season': 1,
        'title_episode': 'title of episode',
        'released': date(2020, 10, 30),
        'number_episode': 1,
        'imdb_rating': 8,
        'language': 'English',

    }
    episode = Episode(**episode_data)
    episode.actors.set([actors.pk])
    episode.genre.set([genre.pk])
    episode.save()
    return episode_data


@pytest.fixture
def episodes(db):
    actors = Actor(name='Name', surname='Actor')
    genre = Genre(name='Genre')
    actors.save()
    genre.save()
    episodes_data = [
        {
            'pk': i,
            'title_serials': 'Title',
            'season': 1,
            'title_episode': f'title of episode {i}',
            'released': date(2020, 10, 30),
            'number_episode': i,
            'imdb_rating': 9 if i > 3 else 5,
            'language': 'English',
        } for i in range(1, 6)
    ]
    for episode_data in episodes_data:
        episode = Episode(**episode_data)
        episode.actors.set([actors.pk])
        episode.genre.set([genre.pk])
        episode.save()
    return episodes_data


@pytest.fixture
def comment(db, episode):
    customer = User(
        username='myuser',
        email='myemail@email.com',
    )
    customer.save()
    episode_instance = Episode(**episode)
    episode_instance.save()
    comment_data = {
        'pk': 1,
        'text': 'comment text',
        'customer': customer,
        'episode': episode_instance,
        'published': date(2020, 10, 30),
    }
    comment = Comment(**comment_data)
    comment.save()
    return comment_data


@pytest.fixture
def comments(db, episode):
    customer = User(
        username='myuser',
        email='myemail@email.com',
    )
    customer.save()
    episode_instance = Episode(**episode)
    episode_instance.save()
    comments_data = [
        {
            'pk': i,
            'text': f'comment text {i}',
            'customer': customer,
            'episode': episode_instance,
            'published': date(2020, 10, 30),
        } for i in range(1, 6)
    ]
    for comment_data in comments_data:
        comment = Comment(**comment_data)
        comment.save()
    return comment_data


@pytest.fixture
def omdb_season():
    response_series = urlopen(f'https://www.omdbapi.com/?i=tt2442560&apikey={api_key}')
    series = json.loads(response_series.read())
    seasons_count = int(series['totalSeasons'])
    return seasons_count
