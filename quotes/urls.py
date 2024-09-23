# quotes/urls.py

from django.urls import path
from . import views

# create a list of URLs for this app:
urlpatterns = [
    path(r'', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all"),
    path(r'about', views.about, name="about"),
]