from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Profile, StatusMessage, Image, Friend
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.urls import reverse

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'


class CreateProfileView(CreateView):
    '''Create a subclass of CreateView to handle profile creation with user registration.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        '''Add the UserCreationForm to the context.'''
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''Process both the UserCreationForm and CreateProfileForm.'''
        # Create User instance
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            # Save the new user
            user = user_form.save()
            
            # Attach user to profile
            form.instance.user = user
            
            # Log the user in
            login(self.request, user)
            
            # Let CreateView handle the rest
            return super().form_valid(form)
        else:
            # If user form is invalid, show both forms again with errors
            return self.form_invalid(form)

    def get_success_url(self):
        '''Redirect to the new user's profile page after successful creation.'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context

    def get_profile(self):
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        form.instance.profile = self.get_profile()
        sm = form.save()
        
        files = self.request.FILES.getlist('files')
        for file in files:
            try:
                img = Image(status_message=sm, image_file=file)
                img.save()
            except Exception as e:
                print(f"Error saving image '{file.name}': {e}")

        return redirect('show_profile', pk=sm.profile.pk)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        other_pk = kwargs.get('other_pk')
        other_profile = get_object_or_404(Profile, pk=other_pk)
        
        profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def dispatch(self, request, *args, **kwargs):
        # Check if the status message belongs to the logged-in user
        status = self.get_object()
        if status.profile.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def dispatch(self, request, *args, **kwargs):
        # Check if the status message belongs to the logged-in user
        status = self.get_object()
        if status.profile.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})