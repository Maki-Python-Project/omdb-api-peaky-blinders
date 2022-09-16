from django.urls import path

from . import views

urlpatterns = [
    path('episodes/', views.EpisodeList.as_view()),
    path('episodes/<int:pk>/', views.EpisodeDetail.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('episodes/imdb/', views.EpisodeImdb.as_view())
    # path('comments/<int:pk>/', views.EpisodeDetail.as_view()),
]
