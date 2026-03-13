from rest_framework import serializers
from .models import Listing


class ListingSerialiser(serializers.ModelSerializer):
    """
    Serialiser for the Listing model.
    Converts Listing objects to JSON and validates incoming data.
    """
    class Meta:
        model = Listing
        fields = '__all__'