from django import forms
from .models import Voter
from datetime import datetime
from django.db import ProgrammingError

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