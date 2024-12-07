# project/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import User, Song, UserGenre, UserSong


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
