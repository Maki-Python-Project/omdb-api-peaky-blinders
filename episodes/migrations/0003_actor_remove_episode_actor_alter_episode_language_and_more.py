# Generated by Django 4.1 on 2022-09-19 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("episodes", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Actor",
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
                ("surname", models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name="episode",
            name="actor",
        ),
        migrations.AlterField(
            model_name="episode",
            name="language",
            field=models.CharField(default="English", max_length=100),
        ),
        migrations.AlterField(
            model_name="episode",
            name="released",
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name="episode",
            name="actors",
            field=models.ManyToManyField(to="episodes.actor"),
        ),
    ]