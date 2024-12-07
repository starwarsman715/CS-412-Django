from django.urls import path
from . import views
from .views import *

app_name = 'project'

urlpatterns = [
    path('', views.home, name='home'),
    
    path('users/', UserListView.as_view(), name='user_list'),
    path('songs/', SongListView.as_view(), name='song_list'),
    
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('songs/<int:pk>/', views.SongDetailView.as_view(), name='song_detail'),
    
    path('add_user/', views.AddUserView.as_view(), name='add_user'),
    path('add_song/', views.SongCreateView.as_view(), name='add_song'),
    
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete_user'),
]
