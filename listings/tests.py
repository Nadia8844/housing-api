from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Listing


class ListingModelTest(TestCase):
    """
    Tests for the Listing database model.
    """

    def setUp(self):
        self.listing = Listing.objects.create(
            title='Test Flat in Leeds',
            address='1 Test Street',
            city='Leeds',
            postcode='LS1 1AA',
            property_type='flat',
            bedrooms=2,
            monthly_rent=900.00,
            available=True,
        )

    def test_listing_created_successfully(self):
        """Tests that a listing is created with the correct fields."""
        self.assertEqual(self.listing.title, 'Test Flat in Leeds')
        self.assertEqual(self.listing.city, 'Leeds')
        self.assertEqual(self.listing.bedrooms, 2)

    def test_listing_string_representation(self):
        """Tests the string representation of a listing."""
        self.assertEqual(str(self.listing), 'Test Flat in Leeds - Leeds')


class ListingAPITest(TestCase):
    """
    Tests for the Listings API endpoints.
    """

    def setUp(self):
        self.client = APIClient()

        # Create a test user for authenticated requests
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

        # Create a sample listing for testing
        self.listing = Listing.objects.create(
            title='Test Flat in Leeds',
            address='1 Test Street',
            city='Leeds',
            postcode='LS1 1AA',
            property_type='flat',
            bedrooms=2,
            monthly_rent=900.00,
            available=True,
        )

    def test_get_all_listings(self):
        """Tests that GET /api/listings/ returns 200 OK."""
        response = self.client.get('/api/listings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_listing(self):
        """Tests that GET /api/listings/{id}/ returns the correct listing."""
        response = self.client.get(f'/api/listings/{self.listing.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['city'], 'Leeds')

    def test_get_listing_not_found(self):
        """Tests that a non-existent listing returns 404."""
        response = self.client.get('/api/listings/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_listing_unauthenticated(self):
        """Tests that an unauthenticated user cannot create a listing."""
        data = {
            'title': 'New Flat',
            'address': '2 New Street',
            'city': 'Manchester',
            'postcode': 'M1 1AA',
            'property_type': 'flat',
            'bedrooms': 1,
            'monthly_rent': 800.00,
            'available': True,
        }
        response = self.client.post('/api/listings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_listing_authenticated(self):
        """Tests that an authenticated user can create a listing."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Flat in Manchester',
            'address': '2 New Street',
            'city': 'Manchester',
            'postcode': 'M1 1AA',
            'property_type': 'flat',
            'bedrooms': 1,
            'monthly_rent': 800.00,
            'available': True,
        }
        response = self.client.post('/api/listings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['city'], 'Manchester')

    def test_update_listing_authenticated(self):
        """Tests that an authenticated user can update a listing."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Flat in Leeds',
            'address': '1 Test Street',
            'city': 'Leeds',
            'postcode': 'LS1 1AA',
            'property_type': 'flat',
            'bedrooms': 2,
            'monthly_rent': 950.00,
            'available': True,
        }
        response = self.client.put(
            f'/api/listings/{self.listing.id}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Flat in Leeds')

    def test_delete_listing_authenticated(self):
        """Tests that an authenticated user can delete a listing."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/listings/{self.listing.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_listings_by_city(self):
        """Tests that listings can be filtered by city."""
        response = self.client.get('/api/listings/?city=Leeds')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for listing in response.data:
            self.assertIn('Leeds', listing['city'])


class AnalyticsAPITest(TestCase):
    """
    Tests for the analytics endpoints.
    """

    def setUp(self):
        self.client = APIClient()
        Listing.objects.create(
            title='Studio in Leeds',
            address='1 Park Row',
            city='Leeds',
            postcode='LS1 1AA',
            property_type='studio',
            bedrooms=0,
            monthly_rent=700.00,
            available=True,
        )
        Listing.objects.create(
            title='Flat in London',
            address='1 Oxford Street',
            city='London',
            postcode='W1 1AA',
            property_type='flat',
            bedrooms=1,
            monthly_rent=2000.00,
            available=True,
        )

    def test_average_rent_endpoint(self):
        """Tests that the average rent endpoint returns 200 OK."""
        response = self.client.get('/api/analytics/average-rent/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_affordability_endpoint(self):
        """Tests that the affordability endpoint returns 200 OK."""
        response = self.client.get('/api/analytics/affordability/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_market_summary_endpoint(self):
        """Tests that the market summary endpoint returns 200 OK."""
        response = self.client.get('/api/analytics/summary/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_market_summary_correct_count(self):
        """Tests that the market summary returns the correct listing count."""
        response = self.client.get('/api/analytics/summary/')
        self.assertEqual(response.data['total_listings'], 2)


class AuthenticationTest(TestCase):
    """
    Tests for user registration and authentication.
    """

    def setUp(self):
        self.client = APIClient()

    def test_register_new_user(self):
        """Tests that a new user can register successfully."""
        response = self.client.post('/api/register/', {
            'username': 'newuser',
            'password': 'securepassword123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_duplicate_username(self):
        """Tests that registering with an existing username returns 400."""
        User.objects.create_user(username='existinguser', password='pass123')
        response = self.client.post('/api/register/', {
            'username': 'existinguser',
            'password': 'newpassword123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_token(self):
        """Tests that a valid user can obtain a JWT token."""
        User.objects.create_user(username='tokenuser', password='pass1234!')
        response = self.client.post('/api/token/', {
            'username': 'tokenuser',
            'password': 'pass1234!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)