# project/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import User, Genre, Song, UserGenre, UserSong

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'birth_date', 'bio']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class UserGenreForm(forms.ModelForm):
    class Meta:
        model = UserGenre
        fields = ['genre']
        widgets = {
            'genre': forms.Select(attrs={'class': 'form-control'}),
        }

class UserSongForm(forms.ModelForm):
    class Meta:
        model = UserSong
        fields = ['song']
        widgets = {
            'song': forms.Select(attrs={'class': 'form-control'}),
        }

# Define formset for genres
UserGenreFormSet = inlineformset_factory(
    User,
    UserGenre,
    form=UserGenreForm,
    extra=2,  # Allow adding up to 2 genres
    max_num=2,  # Limit to exactly 2 genres
    validate_max=True,
    can_delete=False,
)

# Define formset for new users
NewUserSongFormSet = inlineformset_factory(
    User,
    UserSong,
    form=UserSongForm,
    extra=4,  # Show 4 empty forms for new users
    max_num=4,  # Maximum of 4 songs allowed
    validate_max=True,
    can_delete=False,
)

# Define formset for updating existing users
UpdateUserSongFormSet = inlineformset_factory(
    User,
    UserSong,
    form=UserSongForm,
    extra=0,  # No extra forms when updating
    max_num=4,  # Maximum of 4 songs allowed
    validate_max=True,
    can_delete=False,
)

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre', 'release_year', 'youtube_url']
        widgets = {
            'release_year': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'youtube_url': forms.URLInput(attrs={'placeholder': 'https://youtube.com/...'}),
        }