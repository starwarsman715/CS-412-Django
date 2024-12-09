"""
This module defines the database models for a music-based social platform where users can
create profiles, share their music preferences, and match with other users based on musical taste.
The platform supports features like user profiles, genre preferences, favorite songs, and a matching system.

Models:
    - Genre: Represents music genres
    - Profile: Extended user profile information
    - ProfileGenre: Many-to-many relationship between profiles and their preferred genres
    - Song: Music tracks with their metadata
    - ProfileSong: Links between profiles and their favorite songs
    - Match: Represents potential connections between users
    - ShownProfile: Tracks which profiles have been shown to users
"""

from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    """
    Represents a music genre category.
    
    This model stores different music genres that can be associated with songs
    and user preferences. Each genre must have a unique name.
    
    Attributes:
        name (CharField): The name of the genre, limited to 100 characters and must be unique
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """Returns a string representation of the genre name."""
        return self.name

class Profile(models.Model):
    """
    Extends the built-in Django User model with additional profile information.
    
    This model stores additional user information beyond the basic authentication
    details. It maintains a one-to-one relationship with Django's User model and
    includes fields for user preferences and biographical information.
    
    Attributes:
        user (OneToOneField): Link to Django's built-in User model
        username (CharField): Unique username for the profile
        email (EmailField): Unique email address
        birth_date (DateField): User's date of birth
        bio (TextField): Optional biographical information
        created_at (DateTimeField): Timestamp of profile creation
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    birth_date = models.DateField()
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns the username as the string representation."""
        return self.username

class ProfileGenre(models.Model):
    """
    Associates profiles with their preferred music genres.
    
    This is a junction table implementing a many-to-many relationship between
    Profile and Genre models. It allows each profile to have multiple preferred
    genres and each genre to be preferred by multiple profiles.
    
    Attributes:
        profile (ForeignKey): Reference to the Profile model
        genre (ForeignKey): Reference to the Genre model
    
    Meta:
        unique_together ensures a profile can't select the same genre multiple times
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='profile_genres')

    class Meta:
        unique_together = ('profile', 'genre')

    def __str__(self):
        """Returns a string describing the profile-genre relationship."""
        return f"{self.profile.username} prefers {self.genre.name}"

class Song(models.Model):
    """
    Represents a music track with its metadata.
    
    Stores information about individual songs including title, artist, genre,
    release year, and a link to listen to the song on YouTube.
    
    Attributes:
        title (CharField): The name of the song
        artist (CharField): The performer of the song
        genre (ForeignKey): The genre classification of the song
        release_year (PositiveIntegerField): Year the song was released
        youtube_url (URLField): Link to the song on YouTube
    """
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='songs')
    release_year = models.PositiveIntegerField()
    youtube_url = models.URLField()

    def __str__(self):
        """Returns a string combining the song title and artist."""
        return f"{self.title} by {self.artist}"

class ProfileSong(models.Model):
    """
    Associates profiles with their favorite songs.
    
    This model implements a many-to-many relationship between Profile and Song models,
    with additional metadata about when the song was added to favorites. It includes
    a constraint limiting users to a maximum of 5 favorite songs.
    
    Attributes:
        profile (ForeignKey): Reference to the Profile model
        song (ForeignKey): Reference to the Song model
        added_at (DateTimeField): Timestamp when the song was added to favorites
    
    Meta:
        unique_together ensures a profile can't add the same song multiple times
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_songs')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='profile_songs')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'song')

    def __str__(self):
        """Returns a string describing the profile-song relationship."""
        return f"{self.profile.username}'s favorite: {self.song.title}"

    def save(self, *args, **kwargs):
        """
        Override save method to enforce the 5-song limit per profile.
        
        Raises:
            ValueError: If attempting to add more than 4 songs to a profile's favorites
        """
        if not self.pk and ProfileSong.objects.filter(profile=self.profile).count() >= 4:
            raise ValueError("A profile cannot have more than 4 favorite songs.")
        super(ProfileSong, self).save(*args, **kwargs)

class Match(models.Model):
    """
    Represents a potential match between two profiles.
    
    This model handles the matching system between users, tracking who initiated
    the match and its current status. It supports a basic matching workflow with
    pending, accepted, and rejected states.
    
    Attributes:
        sender (ForeignKey): Profile that initiated the match
        receiver (ForeignKey): Profile that received the match request
        created_at (DateTimeField): When the match was initiated
        status (CharField): Current state of the match (pending/accepted/rejected)
    
    Meta:
        unique_together ensures only one match can exist between any two profiles
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_matches')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_matches')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        """Returns a string describing the match and its status."""
        return f"Match from {self.sender.username} to {self.receiver.username} - {self.status}"

class ShownProfile(models.Model):
    """
    Tracks which profiles have been shown to other profiles.
    
    This model maintains a history of profile views to prevent showing the same
    profiles repeatedly and to track user interactions.
    
    Attributes:
        profile (ForeignKey): The profile viewing other profiles
        shown_profile (ForeignKey): The profile that was viewed
        timestamp (DateTimeField): When the profile was shown
    
    Meta:
        unique_together ensures each profile viewing is recorded only once
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='shown_profiles_records')
    shown_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='shown_to_profiles')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'shown_profile')

    def __str__(self):
        """Returns a string describing which profile was shown to whom."""
        return f"{self.profile.username} has seen {self.shown_profile.username}"

def load_data():
    """
    Utility function to populate the database with initial song data.
    
    This function reads song data from a CSV file ('rock_songs.csv') and creates
    corresponding Song and Genre records in the database. It includes error handling
    and progress tracking for bulk data loading.
    
    Process:
        1. Clears existing Song records to prevent duplicates
        2. Reads the CSV file line by line
        3. Creates Genre records as needed
        4. Creates Song records with proper associations
        5. Provides progress updates during loading
    
    Note:
        - Expects a CSV file with headers: title, artist, genre, release_year, spotify_url/youtube_url
        - Prints progress updates every 100 records
        - Handles and reports errors without stopping the entire process
    """
    from .models import Song, Genre
    Song.objects.all().delete()
    print("Deleted existing Song records.")

    import csv
    filename = 'rock_songs.csv'
    count = 0
    
    print("Starting to load data from rock_songs.csv...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        print("CSV Headers:", reader.fieldnames)
        
        for row in reader:
            try:
                if count == 0:
                    print("First row data:", row)
                
                # Extract and clean data from CSV row
                title = row['title'].strip()
                artist = row['artist'].strip()
                genre_name = row['genre'].strip()
                release_year = int(row['release_year'].strip())
                spotify_url = row.get('spotify_url', '').strip() or row.get('youtube_url', '').strip()
                
                # Create or get genre record
                genre, created = Genre.objects.get_or_create(name=genre_name)
                
                # Create song record
                song = Song(
                    title=title,
                    artist=artist,
                    genre=genre,
                    release_year=release_year,
                    spotify_url=spotify_url
                )
                song.save()
                
                count += 1
                if count % 100 == 0:
                    print(f"Processed {count} Song records...")
                    
            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Error message: {str(e)}")
                continue
    
    print(f'Done. Created {count} Song records.')