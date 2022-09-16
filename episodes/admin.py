from django.contrib import admin

from .models import Episode, Comment, Genre


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title_episode', 'season', 'number_episode', 'released',  'imdb_rating'
    )
    list_filter = ('title_episode', 'season', 'number_episode', 'language')
    search_fields = ('title_episode', 'season', 'number_episode')
    save_on_top = True


admin.site.register(Episode, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Genre)
