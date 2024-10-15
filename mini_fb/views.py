from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile  # Retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'  # How to find the data in the template file

class ShowProfilePageView(DetailView):
    '''Create a subclass of DetailView to display a single profile.'''
    model = Profile  # The model to retrieve data from
    template_name = 'mini_fb/show_profile_page.html'  # The template to render
    context_object_name = 'profile'  # The context variable to use in the template

class CreateProfileView(CreateView):
    '''Create a subclass of CreateView to handle profile creation.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(CreateView):
    '''Create a subclass of CreateView to handle status message creation.'''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        '''Add the profile object to the context data.'''
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs.get('pk')
        profile = get_object_or_404(Profile, pk=profile_pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Associate the new status message with the correct profile.'''
        profile_pk = self.kwargs.get('pk')
        profile = get_object_or_404(Profile, pk=profile_pk)
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect to the profile page after successfully posting a status message.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
