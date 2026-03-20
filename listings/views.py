from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Listing
from .serializers import ListingSerialiser


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