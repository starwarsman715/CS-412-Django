# project/urls.py
from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views


app_name = 'project'

urlpatterns = [
    path('', views.home, name='home'),
    
    path('profiles/', ProfileListView.as_view(), name='profile_list'),  # Changed from users to profiles
    path('songs/', SongListView.as_view(), name='song_list'),
    
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),  # Changed from UserDetailView to ProfileDetailView
    path('songs/<int:pk>/', views.SongDetailView.as_view(), name='song_detail'),
    
    path('add_profile/', views.AddProfileView.as_view(), name='add_profile'),  # Changed from add_user to add_profile
    path('add_song/', views.SongCreateView.as_view(), name='add_song'),
    
    path('profiles/<int:pk>/update/', views.ProfileUpdateView.as_view(), name='update_profile'),  # Changed user to profile
    path('profiles/<int:pk>/delete/', views.ProfileDeleteView.as_view(), name='delete_profile'),  # Changed user to profile
    
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='project:home'), name='logout'),
]