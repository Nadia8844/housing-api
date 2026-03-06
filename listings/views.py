from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg, Min, Max, Count
from django.contrib.auth.models import User
from .models import Listing
from .serializers import ListingSerialiser
from decimal import Decimal


class ListingListView(APIView):
    """
    Handles listing all properties and creating a new property.
    GET  /listings/                        - Returns all property listings
    GET  /listings/?city=Leeds             - Filter by city
    GET  /listings/?bedrooms=2             - Filter by number of bedrooms
    GET  /listings/?property_type=flat     - Filter by property type
    GET  /listings/?available=true         - Filter by availability
    POST /listings/                        - Creates a new property listing
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        listings = Listing.objects.all()

        # Filter by city if provided
        city = request.query_params.get('city')
        if city:
            listings = listings.filter(city__icontains=city)

        # Filter by number of bedrooms if provided
        bedrooms = request.query_params.get('bedrooms')
        if bedrooms:
            listings = listings.filter(bedrooms=bedrooms)

        # Filter by property type if provided
        property_type = request.query_params.get('property_type')
        if property_type:
            listings = listings.filter(property_type__icontains=property_type)

        # Filter by availability if provided
        available = request.query_params.get('available')
        if available is not None:
            listings = listings.filter(available=available.lower() == 'true')

        serialiser = ListingSerialiser(listings, many=True)
        return Response(serialiser.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialiser = ListingSerialiser(data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data, status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)


class ListingDetailView(APIView):
    """
    Handles retrieving, updating, and deleting a single property listing.
    GET    /listings/<id>/  - Returns a single listing
    PUT    /listings/<id>/  - Updates a listing
    DELETE /listings/<id>/  - Deletes a listing
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Listing.objects.get(pk=pk)
        except Listing.DoesNotExist:
            return None

    def get(self, request, pk):
        listing = self.get_object(pk)
        if listing is None:
            return Response(
                {"error": "Listing not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serialiser = ListingSerialiser(listing)
        return Response(serialiser.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        listing = self.get_object(pk)
        if listing is None:
            return Response(
                {"error": "Listing not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serialiser = ListingSerialiser(listing, data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data, status=status.HTTP_200_OK)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        listing = self.get_object(pk)
        if listing is None:
            return Response(
                {"error": "Listing not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        listing.delete()
        return Response(
            {"message": "Listing successfully deleted"},
            status=status.HTTP_204_NO_CONTENT
        )
    
class AverageRentByCityView(APIView):
    """
    Analytics endpoint returning average monthly rent per city.
    GET /api/analytics/average-rent/
    """

    def get(self, request):
        results = (
            Listing.objects
            .values('city')
            .annotate(
                average_rent=Avg('monthly_rent'),
                total_listings=Count('id'),
                min_rent=Min('monthly_rent'),
                max_rent=Max('monthly_rent'),
            )
            .order_by('city')
        )
        return Response(results, status=status.HTTP_200_OK)


class AffordabilityView(APIView):
    """
    Analytics endpoint returning an affordability index per city.
    Affordability is calculated as average rent as a percentage
    of the UK median monthly salary (£2,500).
    GET /api/analytics/affordability/
    """
    # UK median monthly take-home salary estimate
    UK_MEDIAN_MONTHLY_SALARY = Decimal('2500.00')

    def get(self, request):
        cities = (
            Listing.objects
            .values('city')
            .annotate(average_rent=Avg('monthly_rent'))
            .order_by('city')
        )

        results = []
        for city in cities:
            affordability_index = round(
                (city['average_rent'] / self.UK_MEDIAN_MONTHLY_SALARY) * 100, 2
            )
            results.append({
                'city': city['city'],
                'average_rent': round(city['average_rent'], 2),
                'affordability_index': affordability_index,
                'affordability_rating': (
                    'affordable' if affordability_index < 30
                    else 'moderate' if affordability_index < 40
                    else 'expensive'
                ),
            })

        return Response(results, status=status.HTTP_200_OK)


class MarketSummaryView(APIView):
    """
    Analytics endpoint returning an overall summary of the housing market.
    GET /api/analytics/summary/
    """

    def get(self, request):
        total_listings = Listing.objects.count()
        available_listings = Listing.objects.filter(available=True).count()
        overall_avg_rent = Listing.objects.aggregate(
            avg=Avg('monthly_rent')
        )['avg']

        summary = {
            'total_listings': total_listings,
            'available_listings': available_listings,
            'unavailable_listings': total_listings - available_listings,
            'overall_average_rent': round(overall_avg_rent, 2),
            'cities_covered': Listing.objects.values('city').distinct().count(),
        }

        return Response(summary, status=status.HTTP_200_OK)
    
class RegisterView(APIView):
    """
    Allows new users to register an account.
    POST /api/register/
    """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password)
        return Response(
            {"message": f"User '{user.username}' registered successfully"},
            status=status.HTTP_201_CREATED
        )