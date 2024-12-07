# project/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Profile, Genre, Song, ProfileGenre, ProfileSong  # Updated imports


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'birth_date', 'bio']
        exclude = ['user']  # Exclude the user field as it will be set programmatically
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
class ProfileGenreForm(forms.ModelForm):  # Changed from UserGenreForm
    class Meta:
        model = ProfileGenre  # Changed from UserGenre
        fields = ['genre']
        widgets = {
            'genre': forms.Select(attrs={'class': 'form-control'}),
        }

class ProfileSongForm(forms.ModelForm):  # Changed from UserSongForm
    class Meta:
        model = ProfileSong  # Changed from UserSong
        fields = ['song']
        widgets = {
            'song': forms.Select(attrs={'class': 'form-control'}),
        }

# Define formset for genres
ProfileGenreFormSet = inlineformset_factory(  # Changed from UserGenreFormSet
    Profile,  # Changed from User
    ProfileGenre,  # Changed from UserGenre
    form=ProfileGenreForm,  # Changed from UserGenreForm
    extra=2,  # Allow adding up to 2 genres
    max_num=2,  # Limit to exactly 2 genres
    validate_max=True,
    can_delete=False,
)

# Define formset for new profiles
NewProfileSongFormSet = inlineformset_factory(  # Changed from NewUserSongFormSet
    Profile,  # Changed from User
    ProfileSong,  # Changed from UserSong
    form=ProfileSongForm,  # Changed from UserSongForm
    extra=4,  # Show 4 empty forms for new profiles
    max_num=4,  # Maximum of 4 songs allowed
    validate_max=True,
    can_delete=False,
)

# Define formset for updating existing profiles
UpdateProfileSongFormSet = inlineformset_factory(  # Changed from UpdateUserSongFormSet
    Profile,  # Changed from User
    ProfileSong,  # Changed from UserSong
    form=ProfileSongForm,  # Changed from UserSongForm
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


class SongSearchForm(forms.Form):
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
        widget=forms.NumberInput(attrs={'placeholder': 'From Year'})
    )
    year_to = forms.IntegerField(
        required=False,
        min_value=1900,
        max_value=2024,
        widget=forms.NumberInput(attrs={'placeholder': 'To Year'})
    )