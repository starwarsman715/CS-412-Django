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
    import csv
    from datetime import datetime
    
    # First, delete all existing records to prevent duplicates
    print("Deleting existing records...")
    Voter.objects.all().delete()
    
    # Update this path to where you saved the CSV file
    filename = 'newton_voters.csv'  # Make sure this path is correct
    
    count = 0
    print("Starting to load data...")
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Convert date strings to datetime objects
                dob = datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date()
                reg_date = datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date()
                
                # Convert voting history to boolean
                v20state = row['v20state'].lower() == 'yes'
                v21town = row['v21town'].lower() == 'yes'
                v21primary = row['v21primary'].lower() == 'yes'
                v22general = row['v22general'].lower() == 'yes'
                v23town = row['v23town'].lower() == 'yes'
                
                voter = Voter(
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row['Residential Address - Apartment Number'] or None,
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=dob,
                    date_of_registration=reg_date,
                    party_affiliation=row['Party Affiliation'],
                    precinct_number=int(row['Precinct Number']),
                    v20state=v20state,
                    v21town=v21town,
                    v21primary=v21primary,
                    v22general=v22general,
                    v23town=v23town,
                    voter_score=int(row['voter_score'])
                )
                
                voter.save()
                count += 1
                
                if count % 1000 == 0:  # Print progress every 1000 records
                    print(f"Processed {count} records...")
                    
            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Error message: {str(e)}")
                continue
    
    print(f'Done. Created {count} Voter records.')