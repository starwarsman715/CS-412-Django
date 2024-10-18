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
