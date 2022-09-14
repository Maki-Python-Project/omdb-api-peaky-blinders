from django.urls import path

from . import views

urlpatterns = [
    path('', views.EpisodeList.as_view()),
    path('<int:pk>/', views.EpisodeDetail.as_view()),
]
