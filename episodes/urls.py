from django.urls import path

from . import views
from .serializers import EpisodeSerializer
from .models import Episode

urlpatterns = [
    path('episodes/', views.EpisodeList.as_view(queryset=Episode.objects.all(), serializer_class=EpisodeSerializer)),
    path('episodes/<int:pk>/', views.EpisodeDetail.as_view()),
    path('episodes/imdb/', views.EpisodeImdb.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
]
