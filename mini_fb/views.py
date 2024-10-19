from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Profile, StatusMessage, Image
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