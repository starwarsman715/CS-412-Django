# In voter_analytics/models.py:
from django.db import models
from datetime import datetime

class Voter(models.Model):
    """
    Store/represent data for a registered voter in Newton, MA.
    """
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Address Fields
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=10)
    
    # Voter Information
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.IntegerField()
    
    # Voting History
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    
    # Derived Field
    voter_score = models.IntegerField()

    def __str__(self):
        """Return a string representation of this voter."""
        return f"{self.first_name} {self.last_name} - {self.street_name}"


def load_data():
    """Function to load voter data records from CSV file into Django model instances."""
    # First, delete existing records to prevent duplicates
    Voter.objects.all().delete()
    print("Deleted existing records.")
    
    import csv
    from datetime import datetime
    
    # Define valid party affiliations
    VALID_PARTIES = {
        'D': 'Democratic',
        'R': 'Republican',
        'CC': 'Constitution Party',
        'L': 'Libertarian Party',
        'T': 'Tea Party',
        'O': 'Other',
        'G': 'Green Party',
        'J': 'Independent Party',
        'Q': 'Reform Party',
        'FF': 'Freedom Party',
        'U': 'Unafiliated'
    }
    
    filename = 'newton_voters.csv'
    count = 0
    print("Starting to load data...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        print("CSV Headers:", reader.fieldnames)
        
        for row in reader:
            try:
                # Debug print first row
                if count == 0:
                    print("First row data:", row)
                
                # Convert date strings to datetime objects
                dob = datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date()
                reg_date = datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date()
                
                # Convert election participation to boolean values
                v20state = str(row['v20state']).strip().upper() == 'TRUE'
                v21town = str(row['v21town']).strip().upper() == 'TRUE'
                v21primary = str(row['v21primary']).strip().upper() == 'TRUE'
                v22general = str(row['v22general']).strip().upper() == 'TRUE'
                v23town = str(row['v23town']).strip().upper() == 'TRUE'
                
                # Debug print for first row
                if count == 0:
                    print("Parsed election data for first row:")
                    print(f"v20state: {row['v20state']} -> {v20state}")
                    print(f"v21town: {row['v21town']} -> {v21town}")
                    print(f"v21primary: {row['v21primary']} -> {v21primary}")
                    print(f"v22general: {row['v22general']} -> {v22general}")
                    print(f"v23town: {row['v23town']} -> {v23town}")
                
                # Calculate voter score
                calculated_score = sum([v20state, v21town, v21primary, v22general, v23town])
                provided_score = int(row['voter_score']) if 'voter_score' in row else calculated_score
                
                if count == 0:
                    print(f"Calculated score: {calculated_score}, Provided score: {provided_score}")
                
                # Handle party affiliation - map non-listed parties to 'O' (Other)
                party = row['Party Affiliation'].strip()
                if party not in VALID_PARTIES:
                    party = 'O'
                
                voter = Voter(
                    first_name=row['First Name'].strip(),
                    last_name=row['Last Name'].strip(),
                    street_number=row['Residential Address - Street Number'].strip(),
                    street_name=row['Residential Address - Street Name'].strip(),
                    apartment_number=row['Residential Address - Apartment Number'].strip() if row['Residential Address - Apartment Number'] else None,
                    zip_code=row['Residential Address - Zip Code'].strip(),
                    date_of_birth=dob,
                    date_of_registration=reg_date,
                    party_affiliation=party,
                    precinct_number=int(row['Precinct Number']),
                    
                    # Store boolean values for election participation
                    v20state=v20state,
                    v21town=v21town,
                    v21primary=v21primary,
                    v22general=v22general,
                    v23town=v23town,
                    
                    # Use calculated score
                    voter_score=calculated_score
                )
                
                voter.save()
                count += 1
                
                if count % 1000 == 0:
                    print(f"Processed {count} records...")
                    
            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Error message: {str(e)}")
                continue
    
    print(f'Done. Created {count} Voter records.')