# project/views.py
from django.shortcuts import render
from django.views.generic import ListView
from .models import User, Song

def home(request):
    return render(request, 'project/home.html')

class UserListView(ListView):
    model = User
    template_name = 'project/user_list.html'  # Specify your template name
    context_object_name = 'users'             # Name of the list in the template
    paginate_by = 8                           # Optional: paginate by 10 users per page

class SongListView(ListView):
    model = Song
    template_name = 'project/song_list.html'  # Specify your template name
    context_object_name = 'songs'             # Name of the list in the template
    paginate_by = 8                           # Optional: paginate by 10 songs per page
