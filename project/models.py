# project/models.py
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    birth_date = models.DateField()
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class UserGenre(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='user_genres')

    class Meta:
        unique_together = ('user', 'genre')

    def __str__(self):
        return f"{self.user.username} prefers {self.genre.name}"

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='songs')
    release_year = models.PositiveIntegerField()
    youtube_url = models.URLField()

    def __str__(self):
        return f"{self.title} by {self.artist}"

class UserSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_songs')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='user_songs')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.song.title}"

    def save(self, *args, **kwargs):
        if not self.pk and UserSong.objects.filter(user=self.user).count() >= 5:
            raise ValueError("A user cannot have more than 5 favorite songs.")
        super(UserSong, self).save(*args, **kwargs)

class Match(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_matches')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_matches')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"Match from {self.sender.username} to {self.receiver.username} - {self.status}"

class Comment(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='comments')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment from {self.sender.username} on {self.match}"

class ShownProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shown_profiles_records')
    shown_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shown_to_users')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'shown_profile')

    def __str__(self):
        return f"{self.user.username} has seen {self.shown_profile.username}"

def load_data():
    """Function to load song data records from a CSV file into Song model instances."""
    # First, delete existing records to prevent duplicates
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
                # Debug print for the first row
                if count == 0:
                    print("First row data:", row)
                
                # Extract fields
                title = row['title'].strip()
                artist = row['artist'].strip()
                genre_name = row['genre'].strip()
                release_year = int(row['release_year'].strip())
                spotify_url = row.get('spotify_url', '').strip() or row.get('youtube_url', '').strip()
                
                # Get or create the genre
                genre, created = Genre.objects.get_or_create(name=genre_name)
                
                # Create and save a new Song instance
                song = Song(
                    title=title,
                    artist=artist,
                    genre=genre,
                    release_year=release_year,
                    spotify_url=spotify_url
                )
                song.save()
                
                count += 1
                # Print progress every 100 records
                if count % 100 == 0:
                    print(f"Processed {count} Song records...")
                    
            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Error message: {str(e)}")
                continue
    
    print(f'Done. Created {count} Song records.')