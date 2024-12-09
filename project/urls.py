"""
URL Configuration for Music Social Platform

It maps URLs to their corresponding views and provides named URL patterns for
reverse URL lookups. The URL structure is organized around main features:
profiles, songs, authentication, and matching system.

URL Structure:
    - Base paths for main features (/profiles/, /songs/)
    - Detail views with primary key parameters
    - Authentication routes (/login/, /logout/)
    - Matching system routes (/swipe/, /matches/)

"""
from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views


app_name = 'project'

urlpatterns = [
    path('', views.home, name='home'),
    
    path('profiles/', ProfileListView.as_view(), name='profile_list'), 
    path('songs/', SongListView.as_view(), name='song_list'),
    
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'), 
    path('songs/<int:pk>/', views.SongDetailView.as_view(), name='song_detail'),
    
    path('add_profile/', views.AddProfileView.as_view(), name='add_profile'),  
    path('add_song/', views.SongCreateView.as_view(), name='add_song'),
    
    path('profiles/<int:pk>/update/', views.ProfileUpdateView.as_view(), name='update_profile'),  
    path('profiles/<int:pk>/delete/', views.ProfileDeleteView.as_view(), name='delete_profile'),  
    
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
    
    path('swipe/', views.SwipeView.as_view(), name='swipe'),
    path('match/<int:receiver_pk>/', views.CreateMatchView.as_view(), name='create_match'),
    path('pass/<int:profile_pk>/', views.PassProfileView.as_view(), name='pass_profile'),
    path('matches/', views.MatchesListView.as_view(), name='matches_list'),
]