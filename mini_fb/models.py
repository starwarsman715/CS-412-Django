from django.db import models

# Create your models here.

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
