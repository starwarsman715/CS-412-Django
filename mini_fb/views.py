from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Existing ShowAllProfilesView
class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile  # Retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'  # How to find the data in the template file

# New ShowProfilePageView
class ShowProfilePageView(DetailView):
    '''Create a subclass of DetailView to display a single profile.'''
    model = Profile  # The model to retrieve data from
    template_name = 'mini_fb/show_profile_page.html'  # The template to render
    context_object_name = 'profile'  # The context variable to use in the template
