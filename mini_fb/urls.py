from django.urls import path
from .views import (
    ShowAllProfilesView,
    ShowProfilePageView,
    CreateProfileView,
    CreateStatusMessageView,
    UpdateProfileView,
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
]