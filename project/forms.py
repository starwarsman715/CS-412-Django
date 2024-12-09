"""
Forms Module for Music Social Platform

It includes forms for profile management, song management, and search functionality.
The module uses Django's built in forms framework and implements inline formsets for handling
related data in a single form submission.

Key Components:
    - Profile creation and management forms
    - Genre and song preference forms
    - Song creation and search forms
    - Inline formsets for handling related data
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Profile, Genre, Song, ProfileGenre, ProfileSong

class ProfileForm(forms.ModelForm):
    """
    Form for creating and updating user profiles.
    
    Handles basic profile information including username, email,
    birth date, and biography. The user field is excluded as it's
    set programmatically during profile creation.
    """
    class Meta:
        model = Profile
        fields = ['username', 'email', 'birth_date', 'bio']
        exclude = ['user']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class ProfileGenreForm(forms.ModelForm):
    """
    Form for managing a user's preferred genres.
    
    Handles the relationship between profiles and music genres.
    Uses a select widget for choosing genres from available options.
    
    """
    class Meta:
        model = ProfileGenre
        fields = ['genre']
        widgets = {
            'genre': forms.Select(attrs={'class': 'form-control'}),
        }

class ProfileSongForm(forms.ModelForm):
    """
    Form for managing a user's favorite songs.
    
    Handles the relationship between profiles and their favorite songs.
    Uses a select widget for choosing songs from available options.
    """
    class Meta:
        model = ProfileSong
        fields = ['song']
        widgets = {
            'song': forms.Select(attrs={'class': 'form-control'}),
        }

# Formset Configurations
# ---------------------
# These formsets handle multiple related model instances in a single form

"""
Formset for managing profile genre preferences.

Configuration:
    - Parent model: Profile
    - Child model: ProfileGenre
    - Maximum of 2 genres per profile
    - Shows 2 empty forms for new entries
    - Validates maximum limit
    - Disables deletion of existing entries
"""
ProfileGenreFormSet = inlineformset_factory(
    Profile,
    ProfileGenre,
    form=ProfileGenreForm,
    extra=2,  # Show 2 empty forms
    max_num=2,  # Maximum of 2 genres
    validate_max=True,
    can_delete=False,
)

"""
Formset for adding songs to new profiles.

Configuration:
    - Parent model: Profile
    - Child model: ProfileSong
    - Maximum of 4 songs per profile
    - Shows 4 empty forms for new entries
    - Validates maximum limit
    - Disables deletion of existing entries
"""
NewProfileSongFormSet = inlineformset_factory(
    Profile,
    ProfileSong,
    form=ProfileSongForm,
    extra=4,  # Show 4 empty forms for new profiles
    max_num=4,  # Maximum of 4 songs
    validate_max=True,
    can_delete=False,
)

"""
Formset for updating song preferences of existing profiles.

Configuration:
    - Parent model: Profile
    - Child model: ProfileSong
    - Maximum of 4 songs per profile
    - No extra empty forms (only show existing entries)
    - Validates maximum limit
    - Disables deletion of existing entries
"""
UpdateProfileSongFormSet = inlineformset_factory(
    Profile,
    ProfileSong,
    form=ProfileSongForm,
    extra=0,  # No extra forms when updating
    max_num=4,
    validate_max=True,
    can_delete=False,
)

class SongForm(forms.ModelForm):
    """
    Form for creating and updating songs.
    
    Handles all song-related data including title, artist, genre,
    release year, and YouTube URL. Implements input validation and
    constraints for numerical and URL fields.
    """
    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre', 'release_year', 'youtube_url']
        widgets = {
            'release_year': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'youtube_url': forms.URLInput(attrs={'placeholder': 'https://youtube.com/...'}),
        }

class SongSearchForm(forms.Form):
    """
    Form for searching and filtering songs.
    
    Provides multiple search criteria:
    - Text search for title/artist
    - Genre filter
    - Year range filter
    
    All fields are optional to allow flexible search combinations.
    Input validation ensures reasonable year ranges and proper data types.
    
    """
    search_query = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Search by title or artist'})
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        empty_label="All Genres"
    )
    year_from = forms.IntegerField(
        required=False,
        min_value=1900,
        max_value=2024,
        widget=forms.NumberInput(attrs={'placeholder': 'From '})
    )
    year_to = forms.IntegerField(
        required=False,
        min_value=1900,
        max_value=2024,
        widget=forms.NumberInput(attrs={'placeholder': 'To '})
    )
    
        
'''
Additioonal documentation of features not used in class:
Fomsets: https://docs.djangoproject.com/en/5.1/topics/forms/formsets/
https://medium.com/@adandan01/django-inline-formsets-example-mybook-420cc4b6225d

'''