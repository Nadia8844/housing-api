from rest_framework import serializers
from .models import Listing, Region


class ListingSerialiser(serializers.ModelSerializer):
    """
    Serialiser for the Listing model.
    Converts Listing objects to JSON and validates incoming data.
    """
    class Meta:
        model = Listing
        fields = '__all__'

class RegionSerialiser(serializers.ModelSerializer):
    """
    Serialiser for the Region model.
    Converts Region objects to JSON and validates incoming data.
    """
    class Meta:
        model = Region
        fields = '__all__'