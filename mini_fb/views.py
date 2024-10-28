from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, StatusMessage, Image, Friend
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.urls import reverse

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile  # Retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'  # How to find the data in the template file

class ShowProfilePageView(DetailView):
    '''Create a subclass of DetailView to display a single profile.'''
    model = Profile  # The model to retrieve data from
    template_name = 'mini_fb/show_profile.html'  # The template to render
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
        '''Associate the new status message with the correct profile and handle image uploads.'''
        # Associate the StatusMessage with the Profile
        profile_pk = self.kwargs.get('pk')
        profile = get_object_or_404(Profile, pk=profile_pk)
        form.instance.profile = profile

        # Save the StatusMessage instance
        sm = form.save()

        # Retrieve the list of uploaded files
        files = self.request.FILES.getlist('files')
        
        for file in files:
            try:
                img = Image(
                    status_message=sm,
                    image_file=file
                )
                img.save()
            except Exception as e:
                print(f"Error saving image '{file.name}': {e}")

        # Redirect to the profile page after processing
        return redirect('show_profile', pk=sm.profile.pk)

    def get_success_url(self):
        '''Redirect to the profile page after successfully posting a status message.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class DeleteStatusMessageView(DeleteView):
    '''Create a subclass of DeleteView to handle status message deletion.'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Redirect to the profile page after successfully deleting a status message.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    '''Create a subclass of UpdateView to handle status message updates.'''
    model = StatusMessage
    fields = ['message']  # Only allow updating the message text
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Redirect to the profile page after successfully updating a status message.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    
class CreateFriendView(View):
    '''Handle the creation of a new friendship between two profiles.'''
    
    def dispatch(self, request, *args, **kwargs):
        # Get the profile IDs from the URL
        profile_pk = kwargs.get('pk')
        other_pk = kwargs.get('other_pk')
        
        # Get the Profile objects
        profile = get_object_or_404(Profile, pk=profile_pk)
        other_profile = get_object_or_404(Profile, pk=other_pk)
        
        # Add the friend relationship
        profile.add_friend(other_profile)
        
        # Redirect back to the original profile page
        return redirect('show_profile', pk=profile_pk)

class ShowFriendSuggestionsView(DetailView):
    '''Display friend suggestions for a profile.'''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'
    

class ShowNewsFeedView(DetailView):
    '''Display news feed for a profile.'''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'