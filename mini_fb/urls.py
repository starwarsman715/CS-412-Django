from django.urls import path
from .views import (
    ShowAllProfilesView,
    ShowProfilePageView,
    CreateProfileView,
    CreateStatusMessageView,
)

urlpatterns = [
    # Existing URL pattern for showing all profiles
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),

    # Existing URL pattern for showing a single profile
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),

    # Existing URL pattern for creating a new profile
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),

    # New URL pattern for creating a new status message
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
]
