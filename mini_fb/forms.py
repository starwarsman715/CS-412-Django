from django import forms
from .models import Profile
from .models import StatusMessage


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url']
        # Optionally, you can customize widgets or labels here
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'email_address': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'profile_image_url': forms.URLInput(attrs={'placeholder': 'Profile Image URL'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'city': 'City',
            'email_address': 'Email Address',
            'profile_image_url': 'Profile Image URL',
        }

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'placeholder': 'What\'s on your mind?',
                'rows': 3,
                'cols': 40,
                'class': 'status-textarea',
            }),
        }
        labels = {
            'message': 'Your Status',
        }
