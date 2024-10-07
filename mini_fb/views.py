from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile
# Create your views here.

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile  # Retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'  # How to find the data in the template file
