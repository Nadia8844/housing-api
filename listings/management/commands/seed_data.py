from django.core.management.base import BaseCommand
from listings.models import Listing


class Command(BaseCommand):
    """
    Management command to populate the database with sample UK housing listings.
    Run with: python3 manage.py seed_data
    """
    help = 'Seeds the database with sample UK housing listings'

    def handle(self, *args, **kwargs):
        # Clear existing listings
        Listing.objects.all().delete()

        sample_listings = [
            {
                'title': 'Modern Studio in Central Leeds',
                'address': '12 Park Row',
                'city': 'Leeds',
                'postcode': 'LS1 5HD',
                'property_type': 'studio',
                'bedrooms': 0,
                'monthly_rent': 750.00,
                'available': True,
            },
            {
                'title': 'Spacious 2-Bed Flat in Manchester',
                'address': '45 Deansgate',
                'city': 'Manchester',
                'postcode': 'M3 4LQ',
                'property_type': 'flat',
                'bedrooms': 2,
                'monthly_rent': 1200.00,
                'available': True,
            },
            {
                'title': 'Victorian Terraced House in Birmingham',
                'address': '78 Moseley Road',
                'city': 'Birmingham',
                'postcode': 'B12 9BT',
                'property_type': 'house',
                'bedrooms': 3,
                'monthly_rent': 1100.00,
                'available': True,
            },
            {
                'title': 'Luxury 1-Bed Flat in London',
                'address': '5 Canary Wharf',
                'city': 'London',
                'postcode': 'E14 5AB',
                'property_type': 'flat',
                'bedrooms': 1,
                'monthly_rent': 2200.00,
                'available': True,
            },
            {
                'title': 'Cosy Cottage in Bristol',
                'address': '22 Clifton Hill',
                'city': 'Bristol',
                'postcode': 'BS8 1BN',
                'property_type': 'house',
                'bedrooms': 2,
                'monthly_rent': 1350.00,
                'available': False,
            },
            {
                'title': '3-Bed Semi-Detached in Sheffield',
                'address': '9 Ecclesall Road',
                'city': 'Sheffield',
                'postcode': 'S11 8TR',
                'property_type': 'house',
                'bedrooms': 3,
                'monthly_rent': 950.00,
                'available': True,
            },
            {
                'title': 'Modern 1-Bed Flat in Edinburgh',
                'address': '33 Princes Street',
                'city': 'Edinburgh',
                'postcode': 'EH2 2AN',
                'property_type': 'flat',
                'bedrooms': 1,
                'monthly_rent': 1050.00,
                'available': True,
            },
            {
                'title': 'Student Studio in Leeds',
                'address': '67 Headingley Lane',
                'city': 'Leeds',
                'postcode': 'LS6 1BJ',
                'property_type': 'studio',
                'bedrooms': 0,
                'monthly_rent': 650.00,
                'available': True,
            },
        ]

        for data in sample_listings:
            Listing.objects.create(**data)
            self.stdout.write(f"Created listing: {data['title']}")

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {len(sample_listings)} listings'
        ))