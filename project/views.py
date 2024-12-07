from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin  # Add this import
from .models import Profile, Song, ProfileGenre, ProfileSong, Genre
from .forms import (ProfileForm, ProfileGenreFormSet, NewProfileSongFormSet,
                   UpdateProfileSongFormSet, SongForm)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def home(request):
    return render(request, 'project/home.html')

# List and Detail views don't need login
class ProfileListView(ListView):
    model = Profile
    template_name = 'project/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 6

class SongListView(ListView):
    model = Song
    template_name = 'project/song_list.html'
    context_object_name = 'songs'
    paginate_by = 6

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['preferred_genres'] = ProfileGenre.objects.filter(profile=profile).select_related('genre')
        context['favorite_songs'] = ProfileSong.objects.filter(profile=profile).select_related('song')
        return context

class SongDetailView(DetailView):
    model = Song
    template_name = 'project/song_detail.html'
    context_object_name = 'song'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = self.object
        context['favorite_users'] = ProfileSong.objects.filter(song=song).select_related('profile')
        return context

# Add LoginRequiredMixin to all Create, Update, and Delete views
class SongCreateView(LoginRequiredMixin, CreateView):
    model = Song
    form_class = SongForm
    template_name = 'project/add_song.html'
    success_url = reverse_lazy('project:song_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Song added successfully!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

# Note: We don't add LoginRequiredMixin to AddProfileView since new users need to create profiles
# project/views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class AddProfileView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'project/add_profile.html'
    success_url = reverse_lazy('project:profile_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add UserCreationForm to context
        context['user_form'] = UserCreationForm()
        # Add formsets
        if self.request.POST:
            context['genre_formset'] = ProfileGenreFormSet(self.request.POST, prefix='genres')
            context['song_formset'] = NewProfileSongFormSet(self.request.POST, prefix='songs')
        else:
            context['genre_formset'] = ProfileGenreFormSet(prefix='genres')
            context['song_formset'] = NewProfileSongFormSet(prefix='songs')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        genre_formset = context['genre_formset']
        song_formset = context['song_formset']
        
        # Create UserCreationForm instance with POST data
        user_form = UserCreationForm(self.request.POST)
        
        if not (user_form.is_valid() and genre_formset.is_valid() and song_formset.is_valid()):
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                # Save the User first
                user = user_form.save()
                
                # Attach user to profile
                self.object = form.save(commit=False)
                self.object.user = user
                self.object.save()
                
                # Save formsets
                genre_formset.instance = self.object
                song_formset.instance = self.object
                genre_formset.save()
                song_formset.save()
                
                # Log the user in
                login(self.request, user)
                
                messages.success(self.request, "Profile created successfully!")
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error creating profile: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'project/update_profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['genre_formset'] = ProfileGenreFormSet(
                self.request.POST,
                instance=self.object,
                prefix='genres'
            )
            context['song_formset'] = UpdateProfileSongFormSet(
                self.request.POST,
                instance=self.object,
                prefix='songs'
            )
        else:
            context['genre_formset'] = ProfileGenreFormSet(
                instance=self.object,
                prefix='genres'
            )
            context['song_formset'] = UpdateProfileSongFormSet(
                instance=self.object,
                prefix='songs'
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        genre_formset = context['genre_formset']
        song_formset = context['song_formset']

        if not (genre_formset.is_valid() and song_formset.is_valid()):
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                self.object = form.save()
                genre_formset.save()
                song_formset.save()

                messages.success(self.request, "Profile updated successfully!")
                return redirect('project:profile_detail', pk=self.object.pk)
                
        except Exception as e:
            messages.error(self.request, f"Error updating profile: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'project/confirm_delete_profile.html'
    success_url = reverse_lazy('project:profile_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Profile deleted successfully!")
        return super().delete(request, *args, **kwargs)