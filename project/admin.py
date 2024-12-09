"""
Django Admin Configuration for Music Social Platform

This module configures the Django admin interface for the music social platform.
It registers all models to make them accessible through Django's built-in
administrative interface, allowing superusers to manage application data.
"""

from django.contrib import admin
from .models import (
    Genre,
    Profile,
    ProfileGenre,
    Song,
    ProfileSong,
    Match,
    ShownProfile
)

# Register all models with default admin configurations
# with basic CRUD operations

admin.site.register(Genre)  # Manage music genres
admin.site.register(Profile)  # Manage user profiles
admin.site.register(ProfileGenre)  # Manage user-genre relationships
admin.site.register(Song)  # Manage song catalog
admin.site.register(ProfileSong)  # Manage user-song relationships
admin.site.register(Match)  # Manage user matches
admin.site.register(ShownProfile)  # Track profile view history