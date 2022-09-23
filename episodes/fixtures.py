import os
import pytest
import json

from urllib.request import urlopen


api_key = os.getenv('API_KEY')


@pytest.fixture
def omdb_season():
    response_series = urlopen(f'https://www.omdbapi.com/?i=tt2442560&apikey={api_key}')
    series = json.loads(response_series.read())
    seasons_count = int(series['totalSeasons'])
    return seasons_count
