from django.views.generic import ListView, DetailView
from django.db.models import Q, Case, When, Value
from .models import Voter
from datetime import datetime

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .forms import VoterFilterForm
from django.db.models import Count
from django.db.models.functions import ExtractYear

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
        queryset = super().get_queryset().order_by('last_name', 'first_name')
        
        # Get filter parameters from GET request
        party = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_birth_year')
        max_year = self.request.GET.get('max_birth_year')
        score = self.request.GET.get('voter_score')
        
        # Apply filters if they exist
        if party:
            queryset = queryset.filter(party_affiliation=party)
            
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
            
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
            
        if score:
            queryset = queryset.filter(voter_score=int(score))
            
        # Check election participation filters
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        for election in elections:
            if self.request.GET.get(election):
                queryset = queryset.filter(**{election: True})
                
        return queryset

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

class VoterGraphsView(ListView):
    """View to display voter analytics graphs"""
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Get filtered queryset
            queryset = self.get_queryset()
            
            # Add filter form to context
            context['form'] = VoterFilterForm(self.request.GET)
            
            # Create graphs
            context['birth_year_graph'] = self.create_birth_year_histogram(queryset)
            context['party_graph'] = self.create_party_pie_chart(queryset)
            context['election_graph'] = self.create_election_histogram(queryset)
            
            # Add summary statistics
            context['voter_count'] = queryset.count()
            
        except Exception as e:
            context['error'] = f"Error generating graphs: {str(e)}"
        
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)
        
        if form.is_valid():
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
        
        return queryset

    def create_birth_year_histogram(self, queryset):
        """Create simple histogram of voter birth years"""
        birth_years = (
            queryset
            .annotate(birth_year=ExtractYear('date_of_birth'))
            .values('birth_year')
            .annotate(count=Count('id'))
            .order_by('birth_year')
        )
        
        fig = go.Figure(data=[
            go.Bar(
                x=[year['birth_year'] for year in birth_years],
                y=[year['count'] for year in birth_years],
                text=[year['count'] for year in birth_years],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Voter Distribution by Birth Year',
            xaxis_title='Birth Year',
            yaxis_title='Number of Voters',
            showlegend=False,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig.to_html(full_html=False)

    def create_party_pie_chart(self, queryset):
        """Create simple pie chart of party affiliations"""
        party_counts = (
            queryset
            .values('party_affiliation')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        fig = go.Figure(data=[
            go.Pie(
                labels=[party['party_affiliation'] for party in party_counts],
                values=[party['count'] for party in party_counts],
                textinfo='label+percent',
            )
        ])
        
        fig.update_layout(
            title='Voter Distribution by Party Affiliation',
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
            showlegend=True
        )
        
        return fig.to_html(full_html=False)

    def create_election_histogram(self, queryset):
        """Create histogram of election participation"""
        elections = {
            'v20state': '2020 State',
            'v21town': '2021 Town',
            'v21primary': '2021 Primary',
            'v22general': '2022 General',
            'v23town': '2023 Town'
        }
        
        participation = []
        for field, name in elections.items():
            count = queryset.filter(**{field: True}).count()
            participation.append({
                'election': name,
                'count': count
            })
        
        fig = go.Figure(data=[
            go.Bar(
                x=[p['election'] for p in participation],
                y=[p['count'] for p in participation],
                text=[p['count'] for p in participation],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Voter Participation by Election',
            xaxis_title='Election',
            yaxis_title='Number of Voters',
            showlegend=False,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig.to_html(full_html=False)