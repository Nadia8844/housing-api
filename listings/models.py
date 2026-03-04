from django.db import models

class Listing(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    property_type = models.CharField(max_length=50)  # e.g. flat, house, studio
    bedrooms = models.IntegerField()
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.city}"
    
class Region(models.Model):
    """
    Represents a UK region with ONS salary and rental data.
    Used for broader regional affordability analysis.
    """
    name = models.CharField(max_length=100, unique=True)
    average_annual_salary = models.DecimalField(max_digits=10, decimal_places=2)
    median_monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)
    population = models.IntegerField()
    country = models.CharField(max_length=50, default='England')

    def __str__(self):
        return self.name