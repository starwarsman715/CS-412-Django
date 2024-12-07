# project/views.py
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.db import transaction
from .models import User, Song, UserGenre, UserSong, Genre
from .forms import UserForm, UserGenreFormSet, UserSongFormSet, SongForm

def home(request):
    return render(request, 'project/home.html')

class UserListView(ListView):
    model = User
    template_name = 'project/user_list.html'  # Specify your template name
    context_object_name = 'users'             # Name of the list in the template
    paginate_by = 6                           # Optional: paginate by 10 users per page

class SongListView(ListView):
    model = Song
    template_name = 'project/song_list.html'  # Specify your template name
    context_object_name = 'songs'             # Name of the list in the template
    paginate_by = 6                         # Optional: paginate by 10 songs per page

# project/views.py

class UserDetailView(DetailView):
    model = User
    template_name = 'project/user_detail.html'  # Specify your template
    context_object_name = 'user_profile'        # Context variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        # Fetch preferred genres
        context['preferred_genres'] = UserGenre.objects.filter(user=user).select_related('genre')
        # Fetch favorite songs
        context['favorite_songs'] = UserSong.objects.filter(user=user).select_related('song')
        return context

# project/views.py

class SongDetailView(DetailView):
    model = Song
    template_name = 'project/song_detail.html'  # Specify your template
    context_object_name = 'song'                # Context variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = self.object
        # Fetch users who have this song as a favorite
        context['favorite_users'] = UserSong.objects.filter(song=song).select_related('user')
        return context

# project/views.py

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
    success_url = reverse_lazy('project:user_list')  # Redirect to user list after success

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['genre_formset'] = UserGenreFormSet(self.request.POST, prefix='genres')
            context['song_formset'] = UserSongFormSet(self.request.POST, prefix='songs')
        else:
            context['genre_formset'] = UserGenreFormSet(prefix='genres')
            context['song_formset'] = UserSongFormSet(prefix='songs')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        genre_formset = context['genre_formset']
        song_formset = context['song_formset']
        with transaction.atomic():
            self.object = form.save()
            if genre_formset.is_valid() and song_formset.is_valid():
                genre_formset.instance = self.object
                song_formset.instance = self.object
                genre_formset.save()
                song_formset.save()
            else:
                return self.form_invalid(form)
        messages.success(self.request, "User created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)