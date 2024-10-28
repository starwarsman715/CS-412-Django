from django.urls import path
from .views import (
    ShowAllProfilesView,
    ShowProfilePageView,
    CreateProfileView,
    CreateStatusMessageView,
    UpdateProfileView,
    DeleteStatusMessageView,
    UpdateStatusMessageView,
    CreateFriendView,
    ShowFriendSuggestionsView,
    ShowNewsFeedView
)

urlpatterns = [
    # URL pattern for showing all profiles
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),

    # URL pattern for showing a single profile
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),

    # URL pattern for creating a new profile
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),

    # URL pattern for creating a new status message
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),

    # URL pattern for updating a profile
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),

    # URL pattern for deleting a status message
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
    
    # URL pattern for updating a status message
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),
    
    # URL pattern for adding a friend
    path('profile/<int:pk>/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend'),
    
    # URL pattern for showing friend suggestions
    path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    
    # URL patter for showing news
    path('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
]