from django.db import models
from django.utils import timezone
from django.urls import reverse 

class Profile(models.Model):
    '''Encapsulate the idea of a Profile for a user.'''

    # Data attributes of a Profile
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=50, blank=False)
    email_address = models.EmailField(blank=False)
    profile_image_url = models.URLField(blank=True)  # New field for image URL

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}'

    def get_status_messages(self):
        '''Return all status messages related to this profile, ordered by timestamp descending.'''
        return self.status_messages.all().order_by('-timestamp')

    def get_absolute_url(self):
        '''Return the URL to access a particular profile instance.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        '''Return a list of all friends' profiles for this profile.'''
        # Get all friendship objects where this profile is either profile1 or profile2
        friends1 = Friend.objects.filter(profile1=self)
        friends2 = Friend.objects.filter(profile2=self)
    
        # Create a list of friend profiles
        friend_profiles = []
    
        # Add profile2s from friends1
        for friendship in friends1:
            friend_profiles.append(friendship.profile2)
        
        # Add profile1s from friends2
        for friendship in friends2:
            friend_profiles.append(friendship.profile1)
        
        return friend_profiles

class StatusMessage(models.Model):
    '''Model representing a user's status message.'''

    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'{self.profile.first_name} {self.profile.last_name} at {self.timestamp}: {self.message[:20]}...'
    
    def get_images(self):
        return self.images.all()

class Image(models.Model):
    '''Encapsulate the idea of an Image associated with a StatusMessage.'''
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image for StatusMessage ID {self.status_message.id} uploaded at {self.uploaded_at}"

class Friend(models.Model):
    '''Encapsulate the idea of a friendship between two profiles.'''
    profile1 = models.ForeignKey(Profile, related_name='profile1', on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name='profile2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        '''Return a string representation of this friendship.'''
        return f'{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}'