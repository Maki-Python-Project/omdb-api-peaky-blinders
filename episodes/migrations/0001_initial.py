# Generated by Django 4.1 on 2022-09-15 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=200)),
                ("published", models.DateField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Comment",
                "verbose_name_plural": "Comments",
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Genre",
                "verbose_name_plural": "Genres",
            },
        ),
        migrations.CreateModel(
            name="Episode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title_serials",
                    models.CharField(default="Peaky Blinders", max_length=400),
                ),
                ("season", models.SmallIntegerField(default=1)),
                ("title_episode", models.CharField(max_length=400)),
                ("released", models.DateField(auto_now_add=True)),
                ("number_episode", models.SmallIntegerField(default=1)),
                ("imdb_rating", models.FloatField(default=5.0)),
                ("actor", models.CharField(default=None, max_length=400)),
                ("language", models.CharField(default="English", max_length=50)),
                ("genre", models.ManyToManyField(to="episodes.genre")),
            ],
            options={
                "verbose_name": "Episode",
                "verbose_name_plural": "Episodes",
            },
        ),
    ]
