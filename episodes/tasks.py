# import requests
from .serializers import EpisodeSerializer
from .models import Episode
from rest_framework.response import Response
from rest_framework import status
from .models import Episode
from celery import shared_task


@shared_task()
def parse_data():
    queryset = Episode.objects.all().values()
    new_data = list(queryset)
    return new_data
    # my_api_key = '5af9b7f2'
    # url = f'http://www.omdbapi.com/?t=Peaky Blinders&type=series&apikey={my_api_key}'
    # response = requests.get(url)
    # if response.status_code == requests.codes.ok and response.json()['Response'] == 'True':
    #     for i in range(int(response.json()['totalSeasons'])):
    #         url += f'&season={i+1}'
    #         response = requests.get(url)
    #         data = {}
    #         for elem in response.json()['Episodes']:
    #             data['id'] = i+10
    #             data['title_episode'] = elem["Title"]
    #             data['season'] = i
    #             data['released'] = elem['Released']
    #             data['genre'] = "Horror"
    #             data['number_episode'] = elem['Episode']
    #             data['imdb_rating'] = elem['imdbRating']
    #         serializer = EpisodeSerializer(data=data)
    #         url = url.replace(f'season={i+1}', "")
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
