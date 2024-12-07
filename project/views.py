from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View  # Added View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.forms import inlineformset_factory
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse

from .models import (
    Profile, 
    Song, 
    ProfileGenre, 
    ProfileSong, 
    Genre,
    Match,           # Added
    ShownProfile     # Added
)
from .forms import (
    ProfileForm, 
    ProfileGenreFormSet, 
    NewProfileSongFormSet,
    UpdateProfileSongFormSet, 
    SongForm, 
    SongSearchForm
)

# Rest of your views remain the same...


def home(request):
    return render(request, 'project/home.html')

# List and Detail views don't need login
class ProfileListView(ListView):
    model = Profile
    template_name = 'project/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 6


class SongListView(ListView):
    model = Song
    template_name = 'project/song_list.html'
    context_object_name = 'songs'
    paginate_by = 6

    def get_queryset(self):
        queryset = Song.objects.all()
        form = SongSearchForm(self.request.GET)
        
        if form.is_valid():
            # Search query for title or artist
            search_query = form.cleaned_data.get('search_query')
            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(artist__icontains=search_query)
                )

            # Filter by genre
            genre = form.cleaned_data.get('genre')
            if genre:
                queryset = queryset.filter(genre=genre)

            # Filter by year range
            year_from = form.cleaned_data.get('year_from')
            if year_from:
                queryset = queryset.filter(release_year__gte=year_from)

            year_to = form.cleaned_data.get('year_to')
            if year_to:
                queryset = queryset.filter(release_year__lte=year_to)

        return queryset.order_by('-release_year')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SongSearchForm(self.request.GET)
        return context
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['preferred_genres'] = ProfileGenre.objects.filter(profile=profile).select_related('genre')
        context['favorite_songs'] = ProfileSong.objects.filter(profile=profile).select_related('song')
        return context

class SongDetailView(DetailView):
    model = Song
    template_name = 'project/song_detail.html'
    context_object_name = 'song'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = self.object
        context['favorite_users'] = ProfileSong.objects.filter(song=song).select_related('profile')
        return context

# Add LoginRequiredMixin to all Create, Update, and Delete views
class SongCreateView(LoginRequiredMixin, CreateView):
    model = Song
    form_class = SongForm
    template_name = 'project/add_song.html'
    success_url = reverse_lazy('project:song_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Song added successfully!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

# Note: We don't add LoginRequiredMixin to AddProfileView since new users need to create profiles
# project/views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class AddProfileView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'project/add_profile.html'
    success_url = reverse_lazy('project:profile_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add UserCreationForm to context
        context['user_form'] = UserCreationForm()
        # Add formsets
        if self.request.POST:
            context['genre_formset'] = ProfileGenreFormSet(self.request.POST, prefix='genres')
            context['song_formset'] = NewProfileSongFormSet(self.request.POST, prefix='songs')
        else:
            context['genre_formset'] = ProfileGenreFormSet(prefix='genres')
            context['song_formset'] = NewProfileSongFormSet(prefix='songs')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        genre_formset = context['genre_formset']
        song_formset = context['song_formset']
        
        # Create UserCreationForm instance with POST data
        user_form = UserCreationForm(self.request.POST)
        
        if not (user_form.is_valid() and genre_formset.is_valid() and song_formset.is_valid()):
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                # Save the User first
                user = user_form.save()
                
                # Attach user to profile
                self.object = form.save(commit=False)
                self.object.user = user
                self.object.save()
                
                # Save formsets
                genre_formset.instance = self.object
                song_formset.instance = self.object
                genre_formset.save()
                song_formset.save()
                
                # Log the user in
                login(self.request, user)
                
                messages.success(self.request, "Profile created successfully!")
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error creating profile: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'project/update_profile.html'
    
    def get_context_data(self, **kwargs):
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
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'project/confirm_delete_profile.html'
    success_url = reverse_lazy('project:profile_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Profile deleted successfully!")
        return super().delete(request, *args, **kwargs)
    
class SwipeView(LoginRequiredMixin, View):
    def get(self, request):
        # Get the current user's profile
        current_profile = request.user.profile
        
        # Get the ID of the last viewed profile from the session
        last_viewed_id = request.session.get('last_viewed_profile_id', 0)
        
        # Get profiles that have been matched with current user
        matched_profiles = Match.objects.filter(
            Q(sender=current_profile) |
            Q(receiver=current_profile)
        ).values_list('sender', 'receiver')
        
        # Flatten and combine sender and receiver IDs
        matched_ids = set()
        for sender_id, receiver_id in matched_profiles:
            matched_ids.add(sender_id)
            matched_ids.add(receiver_id)

        # Get next profile after the last viewed ID
        potential_matches = Profile.objects.exclude(
            id__in=matched_ids
        ).exclude(
            id=current_profile.id
        ).filter(
            profile_genres__genre__in=current_profile.profile_genres.values('genre'),
            id__gt=last_viewed_id
        ).order_by('id')

        # If no more profiles after last_viewed_id, start over from beginning
        if not potential_matches.exists():
            potential_matches = Profile.objects.exclude(
                id__in=matched_ids
            ).exclude(
                id=current_profile.id
            ).filter(
                profile_genres__genre__in=current_profile.profile_genres.values('genre')
            ).order_by('id')
            # Reset last viewed ID
            last_viewed_id = 0

        if potential_matches.exists():
            profile_to_show = potential_matches.first()
            # Store the current profile ID in session
            request.session['last_viewed_profile_id'] = profile_to_show.id
            return render(request, 'project/swipe.html', {
                'profile': profile_to_show
            })
        else:
            messages.info(request, "No more profiles to show right now!")
            return redirect('project:profile_list')
class CreateMatchView(LoginRequiredMixin, View):
    def post(self, request, receiver_pk):
        try:
            sender_profile = request.user.profile
            receiver_profile = Profile.objects.get(pk=receiver_pk)
            
            # Check if a match already exists
            existing_match = Match.objects.filter(
                Q(sender=sender_profile, receiver=receiver_profile) |
                Q(sender=receiver_profile, receiver=sender_profile)
            ).first()
            
            if existing_match:
                if existing_match.sender == receiver_profile:
                    # Other person already liked current user
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
    def post(self, request, profile_pk):
        # Store the passed profile ID in session
        request.session['last_viewed_profile_id'] = profile_pk
        return redirect('project:swipe')
class MatchesListView(LoginRequiredMixin, ListView):
    template_name = 'project/matches_list.html'
    context_object_name = 'matches'

    def get_queryset(self):
        return Match.objects.filter(
            Q(sender=self.request.user.profile, status='accepted') |
            Q(receiver=self.request.user.profile, status='accepted')
        )