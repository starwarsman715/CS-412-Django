from django.urls import path
from . import views
from .views import *

app_name = 'project'

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('songs/', SongListView.as_view(), name='song_list'),
]
