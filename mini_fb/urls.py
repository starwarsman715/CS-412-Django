# mini_fb/urls.py

from django.urls import path
from .views import ShowAllProfilesView  # Our view class definition

urlpatterns = [
    # Map the root URL to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),  # Generic class-based view
]
