# voter_analytics/forms.py
from django import forms
from .models import Voter
from datetime import datetime
from django.db import ProgrammingError

class VoterFilterForm(forms.Form):
    # Party affiliation dropdown
    PARTY_CHOICES = [('', 'All Parties')] + list(Voter.objects.values_list('party_affiliation', 'party_affiliation').distinct())
    party_affiliation = forms.ChoiceField(choices=PARTY_CHOICES, required=False)
    
    # Birth year ranges
    current_year = datetime.now().year
    YEAR_CHOICES = [('', 'Any')] + [(str(year), str(year)) for year in range(1900, current_year + 1)]
    min_birth_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    max_birth_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    
    # Voter score dropdown
    SCORE_CHOICES = [('', 'Any')] + [(str(i), str(i)) for i in range(6)]  # 0 to 5
    voter_score = forms.ChoiceField(choices=SCORE_CHOICES, required=False)
    
    # Election participation checkboxes
    v20state = forms.BooleanField(required=False, label='2020 State Election')
    v21town = forms.BooleanField(required=False, label='2021 Town Election')
    v21primary = forms.BooleanField(required=False, label='2021 Primary')
    v22general = forms.BooleanField(required=False, label='2022 General')
    v23town = forms.BooleanField(required=False, label='2023 Town Election')

# voter_analytics/views.py
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Voter
from .forms import VoterFilterForm
from datetime import datetime

class VoterListView(ListView):
    """View to display voter listing with filters"""
    template_name = 'voter_analytics/voter_list.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)
        
        if form.is_valid():
            # Apply filters based on form data
            if party := form.cleaned_data.get('party_affiliation'):
                queryset = queryset.filter(party_affiliation=party)
                
            if min_year := form.cleaned_data.get('min_birth_year'):
                queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
                
            if max_year := form.cleaned_data.get('max_birth_year'):
                queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
                
            if score := form.cleaned_data.get('voter_score'):
                queryset = queryset.filter(voter_score=int(score))
                
            # Election participation filters
            for election in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if form.cleaned_data.get(election):
                    queryset = queryset.filter(**{election: True})
        
        return queryset.order_by('last_name', 'first_name')

class VoterDetailView(DetailView):
    """View to display details of a single voter"""
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voter = self.get_object()
        # Create Google Maps URL for the address
        address = f"{voter.street_number}+{voter.street_name}+Newton+MA+{voter.zip_code}"
        context['map_url'] = f"https://www.google.com/maps/search/?api=1&query={address}"
        return context

class VoterFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get party choices dynamically, handle case where table doesn't exist yet
        try:
            PARTY_CHOICES = [('', 'All Parties')] + list(Voter.objects.values_list('party_affiliation', 'party_affiliation').distinct())
        except ProgrammingError:
            PARTY_CHOICES = [('', 'All Parties')]
        self.fields['party_affiliation'].choices = PARTY_CHOICES

    # Birth year ranges
    current_year = datetime.now().year
    YEAR_CHOICES = [('', 'Any')] + [(str(year), str(year)) for year in range(1900, current_year + 1)]
    
    # Form field definitions
    party_affiliation = forms.ChoiceField(choices=[], required=False)  # Choices set in __init__
    min_birth_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    max_birth_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    
    # Voter score dropdown
    SCORE_CHOICES = [('', 'Any')] + [(str(i), str(i)) for i in range(6)]  # 0 to 5
    voter_score = forms.ChoiceField(choices=SCORE_CHOICES, required=False)
    
    # Election participation checkboxes
    v20state = forms.BooleanField(required=False, label='2020 State Election')
    v21town = forms.BooleanField(required=False, label='2021 Town Election')
    v21primary = forms.BooleanField(required=False, label='2021 Primary')
    v22general = forms.BooleanField(required=False, label='2022 General')
    v23town = forms.BooleanField(required=False, label='2023 Town Election')