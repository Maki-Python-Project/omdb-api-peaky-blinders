from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self) -> str:
        return self.name


class Episode(models.Model):
    title_serials = models.CharField(max_length=400, default='Peaky Blinders')
    season = models.SmallIntegerField(default=1)
    title_episode = models.CharField(max_length=400)
    released = models.DateField(auto_now_add=True)
    number_episode = models.SmallIntegerField(default=1)
    imdb_rating = models.FloatField(default=5.0)
    genre = models.ManyToManyField(Genre)
    actor = models.CharField(max_length=400, default=None)
    language = models.CharField(max_length=50, default='English')

    class Meta:
        verbose_name = "Episode"
        verbose_name_plural = "Episodes"

    def __str__(self) -> str:
        return self.title_episode


class Comment(models.Model):
    text = models.CharField(max_length=200)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(
        Episode, related_name='comments', null=True, on_delete=models.CASCADE
    )
    published = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self) -> str:
        return f'{self.text}; author: {self.customer}'
