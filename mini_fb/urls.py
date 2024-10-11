from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView  # Import the new view

urlpatterns = [
    # Existing URL pattern for showing all profiles
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    
    # New URL pattern for showing a single profile
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
]
