# project/admin.py
from django.contrib import admin
from .models import (
    Genre, User, UserGenre, Song, UserSong, Match, Comment, ShownProfile
)

admin.site.register(Genre)
admin.site.register(User)
admin.site.register(UserGenre)
admin.site.register(Song)
admin.site.register(UserSong)
admin.site.register(Match)
admin.site.register(Comment)
admin.site.register(ShownProfile)
