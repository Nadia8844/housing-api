from django.urls import path
from .views import (
    ListingListView,
    ListingDetailView,
    AverageRentByCityView,
    AffordabilityView,
    MarketSummaryView,
    RegisterView,
    RegionListView,
    RegionDetailView,
)

urlpatterns = [
    path('listings/', ListingListView.as_view(), name='listing-list'),
    path('listings/<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
    path('analytics/average-rent/', AverageRentByCityView.as_view(), name='average-rent'),
    path('analytics/affordability/', AffordabilityView.as_view(), name='affordability'),
    path('analytics/summary/', MarketSummaryView.as_view(), name='market-summary'),
    path('register/', RegisterView.as_view(), name='register'),
    path('regions/', RegionListView.as_view(), name='region-list'),
    path('regions/<int:pk>/', RegionDetailView.as_view(), name='region-detail'),
]