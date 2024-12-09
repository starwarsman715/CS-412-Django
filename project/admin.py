# project/admin.py
from django.contrib import admin
from .models import (
    Genre, Profile, ProfileGenre, Song, ProfileSong, Match, ShownProfile
)

admin.site.register(Genre)
admin.site.register(Profile)
admin.site.register(ProfileGenre)
admin.site.register(Song)
admin.site.register(ProfileSong)
admin.site.register(Match)
admin.site.register(ShownProfile)