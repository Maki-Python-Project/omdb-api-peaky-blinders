from django.contrib import admin

from .models import Episode, Comment, Genre

admin.site.register(Episode)
admin.site.register(Comment)
admin.site.register(Genre)
