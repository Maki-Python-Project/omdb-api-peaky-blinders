# Generated by Django 4.1 on 2022-09-14 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("episodes", "0004_comment_published"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="published",
            field=models.DateField(),
        ),
    ]
