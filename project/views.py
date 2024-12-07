# project/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.db import transaction
from .models import Profile, Song, ProfileGenre, ProfileSong, Genre  # Updated imports
from .forms import (ProfileForm, ProfileGenreFormSet, NewProfileSongFormSet,  # These will need to be updated in forms.py
                   UpdateProfileSongFormSet, SongForm)

def home(request):
    return render(request, 'project/home.html')

class ProfileListView(ListView):  # Changed from UserListView
    model = Profile
    template_name = 'project/profile_list.html'  # Will need to rename template
    context_object_name = 'profiles'  # Changed from users
    paginate_by = 6

class SongListView(ListView):
    model = Song
    template_name = 'project/song_list.html'
    context_object_name = 'songs'
    paginate_by = 6

class ProfileDetailView(DetailView):  # Changed from UserDetailView
    model = Profile
    template_name = 'project/profile_detail.html'  # Will need to rename template
    context_object_name = 'profile'  # Changed from user_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['preferred_genres'] = ProfileGenre.objects.filter(profile=profile).select_related('genre')  # Changed from UserGenre and user
        context['favorite_songs'] = ProfileSong.objects.filter(profile=profile).select_related('song')  # Changed from UserSong and user
        return context

class SongDetailView(DetailView):
    model = Song
    template_name = 'project/song_detail.html'
    context_object_name = 'song'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = self.object
        context['favorite_users'] = ProfileSong.objects.filter(song=song).select_related('profile')  # Changed from UserSong and user
        return context

class SongCreateView(CreateView):
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

class AddProfileView(CreateView):  # Changed from AddUserView
    model = Profile
    form_class = ProfileForm  # Changed from UserForm
    template_name = 'project/add_profile.html'  # Will need to rename template
    success_url = reverse_lazy('project:profile_list')  # Changed from user_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['genre_formset'] = ProfileGenreFormSet(self.request.POST, prefix='genres')  # Changed from UserGenreFormSet
            context['song_formset'] = NewProfileSongFormSet(self.request.POST, prefix='songs')  # Changed from NewUserSongFormSet
        else:
            context['genre_formset'] = ProfileGenreFormSet(prefix='genres')
            context['song_formset'] = NewProfileSongFormSet(prefix='songs')
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
                genre_formset.instance = self.object
                song_formset.instance = self.object
                genre_formset.save()
                song_formset.save()
                
                messages.success(self.request, "Profile created successfully!")  # Changed message
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error creating profile: {str(e)}")  # Changed message
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class ProfileUpdateView(UpdateView):  # Changed from UserUpdateView
    model = Profile
    form_class = ProfileForm  # Changed from UserForm
    template_name = 'project/update_profile.html'  # Will need to rename template
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['genre_formset'] = ProfileGenreFormSet(  # Changed from UserGenreFormSet
                self.request.POST,
                instance=self.object,
                prefix='genres'
            )
            context['song_formset'] = UpdateProfileSongFormSet(  # Changed from UpdateUserSongFormSet
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
                return redirect('project:profile_detail', pk=self.object.pk)  # Changed from user_detail
                
        except Exception as e:
            messages.error(self.request, f"Error updating profile: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class ProfileDeleteView(DeleteView):  # Changed from UserDeleteView
    model = Profile
    template_name = 'project/confirm_delete_profile.html'  # Will need to rename template
    success_url = reverse_lazy('project:profile_list')  # Changed from user_list

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Profile deleted successfully!")  # Changed message
        return super().delete(request, *args, **kwargs)