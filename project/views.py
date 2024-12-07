# project/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.db import transaction
from .models import User, Song, UserGenre, UserSong, Genre
from .forms import (UserForm, UserGenreFormSet, NewUserSongFormSet, 
                   UpdateUserSongFormSet, SongForm)

def home(request):
    return render(request, 'project/home.html')

class UserListView(ListView):
    model = User
    template_name = 'project/user_list.html'
    context_object_name = 'users'
    paginate_by = 6

class SongListView(ListView):
    model = Song
    template_name = 'project/song_list.html'
    context_object_name = 'songs'
    paginate_by = 6

class UserDetailView(DetailView):
    model = User
    template_name = 'project/user_detail.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['preferred_genres'] = UserGenre.objects.filter(user=user).select_related('genre')
        context['favorite_songs'] = UserSong.objects.filter(user=user).select_related('song')
        return context

class SongDetailView(DetailView):
    model = Song
    template_name = 'project/song_detail.html'
    context_object_name = 'song'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = self.object
        context['favorite_users'] = UserSong.objects.filter(song=song).select_related('user')
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

class AddUserView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'project/add_user.html'
    success_url = reverse_lazy('project:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['genre_formset'] = UserGenreFormSet(self.request.POST, prefix='genres')
            context['song_formset'] = NewUserSongFormSet(self.request.POST, prefix='songs')
        else:
            context['genre_formset'] = UserGenreFormSet(prefix='genres')
            context['song_formset'] = NewUserSongFormSet(prefix='songs')
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
                
                messages.success(self.request, "User created successfully!")
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error creating user: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'project/update_user.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['genre_formset'] = UserGenreFormSet(
                self.request.POST,
                instance=self.object,
                prefix='genres'
            )
            context['song_formset'] = UpdateUserSongFormSet(
                self.request.POST,
                instance=self.object,
                prefix='songs'
            )
        else:
            context['genre_formset'] = UserGenreFormSet(
                instance=self.object,
                prefix='genres'
            )
            context['song_formset'] = UpdateUserSongFormSet(
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
                return redirect('project:user_detail', pk=self.object.pk)
                
        except Exception as e:
            messages.error(self.request, f"Error updating profile: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class UserDeleteView(DeleteView):
    model = User
    template_name = 'project/confirm_delete_user.html'
    success_url = reverse_lazy('project:user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "User deleted successfully!")
        return super().delete(request, *args, **kwargs)