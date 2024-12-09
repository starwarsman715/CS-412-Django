"""
Music Social Platform Views Module

It provides views for user profiles, songs, matching system, and authentication handling.
The views support both authenticated and non-authenticated access with appropriate
permissions and implement complex features like profile matching and music preferences.

Key Features:
    - Profile management (CRUD operations)
    - Song catalog browsing and searching
    - User matching system with swipe functionality
    - Genre and song preference management
    - Authentication integration
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import (
    Profile, 
    Song, 
    ProfileGenre, 
    ProfileSong, 
    Match
)
from .forms import (
    ProfileForm, 
    ProfileGenreFormSet, 
    NewProfileSongFormSet,
    UpdateProfileSongFormSet, 
    SongForm, 
    SongSearchForm
)

def home(request):
    """
    Renders the application's home page.
    """
    return render(request, 'project/home.html')

class ProfileListView(ListView):
    """
    Displays a paginated list of user profiles.
    
    This view is accessible to all users (authenticated and non-authenticated).
    Profiles are displayed in a paginated format with 6 profiles per page.
    
    """
    model = Profile
    template_name = 'project/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 6

class SongListView(ListView):
    """
    Displays a searchable, filterable list of songs.
    
    Implements advanced search functionality including:
    - Text search for title or artist
    - Genre filtering
    - Year range filtering
    
    """
    model = Song
    template_name = 'project/song_list.html'
    context_object_name = 'songs'
    paginate_by = 6

    def get_queryset(self):
        """
        Filters and returns the queryset based on search parameters.
        """
        queryset = Song.objects.all()
        form = SongSearchForm(self.request.GET)
        
        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(artist__icontains=search_query)
                )

            genre = form.cleaned_data.get('genre')
            if genre:
                queryset = queryset.filter(genre=genre)

            year_from = form.cleaned_data.get('year_from')
            if year_from:
                queryset = queryset.filter(release_year__gte=year_from)

            year_to = form.cleaned_data.get('year_to')
            if year_to:
                queryset = queryset.filter(release_year__lte=year_to)

        return queryset.order_by('-release_year')

    def get_context_data(self, **kwargs):
        """
        Adds the search form to the template context.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = SongSearchForm(self.request.GET)
        return context

class ProfileDetailView(DetailView):
    """
    Displays detailed information about a specific user profile.
    
    Shows profile information along with their preferred genres
    and favorite songs using related data.
    """
    model = Profile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        """
        Enhances the context with related genre and song information.
        
        Adds the profile's preferred genres and favorite songs to the
        template context using database queries.
        """
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['preferred_genres'] = ProfileGenre.objects.filter(profile=profile).select_related('genre')
        context['favorite_songs'] = ProfileSong.objects.filter(profile=profile).select_related('song')
        return context

class SongDetailView(DetailView):
    """
    Displays detailed information about a specific song.
    
    Shows song information along with a list of users who
    have marked it as a favorite.
    """
    model = Song
    template_name = 'project/song_detail.html'
    context_object_name = 'song'

    def get_context_data(self, **kwargs):
        """
        Enhances the context with related user information.
        
        Adds a list of users who have favorited the song to the
        template context using database queries.
        
        """
        context = super().get_context_data(**kwargs)
        song = self.object
        context['favorite_users'] = ProfileSong.objects.filter(song=song).select_related('profile')
        return context

class SongCreateView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of new songs.
    
    Requires authentication. Provides feedback messages for
    successful creation or validation errors.
    
    """
    model = Song
    form_class = SongForm
    template_name = 'project/add_song.html'
    success_url = reverse_lazy('project:song_list')
    
    def form_valid(self, form):
        """
        Handles successful form validation.
        """
        messages.success(self.request, "Song added successfully!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        Handles form validation failure.
        """
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class AddProfileView(CreateView):
    """
    Handles user registration and profile creation.
    
    This view manages the creation of both a Django User instance
    and an associated Profile instance. It handles multiple forms:
    - User creation form
    - Profile form
    - Genre preferences formset
    - Favorite songs formset
    """
    model = Profile
    form_class = ProfileForm
    template_name = 'project/add_profile.html'
    success_url = reverse_lazy('project:profile_list')

    def get_context_data(self, **kwargs):
        """
        Prepares forms and formsets for the template.
        
        Creates or processes user form and formsets for genre
        preferences and favorite songs.
        
        """
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        
        if self.request.POST:
            context['genre_formset'] = ProfileGenreFormSet(self.request.POST, prefix='genres')
            context['song_formset'] = NewProfileSongFormSet(self.request.POST, prefix='songs')
        else:
            context['genre_formset'] = ProfileGenreFormSet(prefix='genres')
            context['song_formset'] = NewProfileSongFormSet(prefix='songs')
        return context

    def form_valid(self, form):
        """
        Processes valid form submission.
        
        Handles the creation of User and Profile instances along with
        their related data (genres and songs) within a transaction.
        Also logs in the new user upon successful creation.
        """
        context = self.get_context_data()
        genre_formset = context['genre_formset']
        song_formset = context['song_formset']
        user_form = UserCreationForm(self.request.POST)
        
        if not (user_form.is_valid() and genre_formset.is_valid() and song_formset.is_valid()):
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                user = user_form.save()
                self.object = form.save(commit=False)
                self.object.user = user
                self.object.save()
                
                genre_formset.instance = self.object
                song_formset.instance = self.object
                genre_formset.save()
                song_formset.save()
                
                login(self.request, user)
                
                messages.success(self.request, "Profile created successfully!")
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error creating profile: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Handles form validation failure.
        """
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Handles profile updates for authenticated users.
    
    Manages updates to profile information, genre preferences,
    and favorite songs. Uses transactions to ensure data consistency.
    """
    model = Profile
    form_class = ProfileForm
    template_name = 'project/update_profile.html'
    
    def get_context_data(self, **kwargs):
        """
        Prepares forms and formsets for the template.
        
        Creates or processes formsets for genre preferences
        and favorite songs with existing data.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['genre_formset'] = ProfileGenreFormSet(
                self.request.POST,
                instance=self.object,
                prefix='genres'
            )
            context['song_formset'] = UpdateProfileSongFormSet(
                self.request.POST,
                instance=self.object,
                prefix='songs'
            )
        else:
            context['genre_formset'] = ProfileGenreFormSet(
                instance=self.object,
                prefix='genres'
            )
            context['song_formset'] = UpdateProfileSongFormSet(
                instance=self.object,
                prefix='songs'
            )
        return context

    def form_valid(self, form):
        """
        Processes valid form submission.
        
        Updates profile data along with related genres and songs
        within a transaction.
        
        """
        context = self.get_context_data()
        genre_formset = context['genre_formset']
        song_formset = context['song_formset']

        if not (genre_formset.is_valid() and song_formset.is_valid()):
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                self.object = form.save()
                genre_formset.save()
                song_formset.save()

                messages.success(self.request, "Profile updated successfully!")
                return redirect('project:profile_detail', pk=self.object.pk)
                
        except Exception as e:
            messages.error(self.request, f"Error updating profile: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Handles form validation failure.
        
        """
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handles profile deletion for authenticated users.
    
    Provides confirmation page before deletion and redirects
    to profile list after successful deletion.
    
    """
    model = Profile
    template_name = 'project/confirm_delete_profile.html'
    success_url = reverse_lazy('project:profile_list')

    def delete(self, request, *args, **kwargs):
        """
        Processes profile deletion.
        """
        messages.success(self.request, "Profile deleted successfully!")
        return super().delete(request, *args, **kwargs)

class SwipeView(LoginRequiredMixin, View):
    """
    Implements the profile matching interface.
    
    Manages the display of potential matches to users, tracking viewed profiles
    and handling match status. Implements a "swipe" mechanism similar to real dating apps.
    
    Required Authentication: Yes
    """
    def get(self, request):
        """
        Displays the next potential match to the user.
        
        Implements complex matching logic:
        1. Excludes already matched profiles
        2. Excludes previously seen profiles
        3. Implements pagination through profile list
        4. Resets to beginning when all profiles are viewed
        
        """
        current_profile = request.user.profile
        last_viewed_id = request.session.get('last_viewed_profile_id', 0)
        
        # Get profiles with completed or pending matches
        matched_profiles = Match.objects.filter(
            (Q(sender=current_profile) & Q(status='accepted')) |  
            (Q(receiver=current_profile) & Q(status='accepted')) |  
            (Q(sender=current_profile) & Q(status='pending'))  
        ).values_list('sender', 'receiver')
        
        # Combine all profiles to exclude
        matched_ids = set()
        for sender_id, receiver_id in matched_profiles:
            matched_ids.add(sender_id)
            matched_ids.add(receiver_id)

        # Find next potential match
        potential_matches = Profile.objects.exclude(
            id__in=matched_ids
        ).exclude(
            id=current_profile.id
        ).filter(
            id__gt=last_viewed_id
        ).order_by('id')

        # Reset to beginning if needed
        if not potential_matches.exists():
            potential_matches = Profile.objects.exclude(
                id__in=matched_ids
            ).exclude(
                id=current_profile.id
            ).order_by('id')
            last_viewed_id = 0

        if potential_matches.exists():
            profile_to_show = potential_matches.first()
            request.session['last_viewed_profile_id'] = profile_to_show.id
            return render(request, 'project/swipe.html', {
                'profile': profile_to_show
            })
        else:
            messages.info(request, "No more profiles to show right now!")
            return redirect('project:profile_list')

class CreateMatchView(LoginRequiredMixin, View):
    """
    Handles the creation and updating of matches between profiles.
    
    Manages the matching logic when a user "swipes right" on another profile.
    Handles both new matches and updating existing matches when mutual interest
    is shown.
    
    Required Authentication: Yes
    """
    def post(self, request, receiver_pk):
        """
        Processes a user's interest in another profile.
        
        Implements the following logic:
        1. Checks for existing matches
        2. Creates new pending matches
        3. Updates to accepted status if mutual interest
        
        """
        try:
            sender_profile = request.user.profile
            receiver_profile = Profile.objects.get(pk=receiver_pk)
            
            # Check for existing match
            existing_match = Match.objects.filter(
                Q(sender=sender_profile, receiver=receiver_profile) |
                Q(sender=receiver_profile, receiver=sender_profile)
            ).first()
            
            if existing_match:
                if existing_match.sender == receiver_profile:
                    # Convert to mutual match
                    existing_match.status = 'accepted'
                    existing_match.save()
                    messages.success(request, f"It's a match with {receiver_profile.username}!")
                else:
                    messages.info(request, "You already liked this profile!")
            else:
                # Create new pending match
                Match.objects.create(
                    sender=sender_profile,
                    receiver=receiver_profile,
                    status='pending'
                )
                messages.success(request, f"You liked {receiver_profile.username}!")
            
            return redirect('project:swipe')
            
        except Profile.DoesNotExist:
            messages.error(request, "Profile not found!")
            return redirect('project:swipe')

class PassProfileView(LoginRequiredMixin, View):
    """
    Handles "swipe left" actions when a user passes on a profile.
    
    Tracks viewed profiles to maintain viewing history and prevent
    repeated displays of the same profile.
    
    Required Authentication: Yes
    """
    def post(self, request, profile_pk):
        """
        Records a passed profile and moves to the next one.
        """
        request.session['last_viewed_profile_id'] = profile_pk
        return redirect('project:swipe')

class MatchesListView(LoginRequiredMixin, ListView):
    """
    Displays a list of successful matches for the current user.
    
    Shows all profiles where there is mutual interest (accepted matches),
    either initiated by the current user or by other users.
        
    Required Authentication: Yes
    """
    template_name = 'project/matches_list.html'
    context_object_name = 'matches'

    def get_queryset(self):
        """
        Retrieves all accepted matches for the current user.
        """
        return Match.objects.filter(
            Q(sender=self.request.user.profile, status='accepted') |
            Q(receiver=self.request.user.profile, status='accepted')
        )