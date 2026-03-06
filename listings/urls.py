from django.urls import path
from .views import (
    ListingListView,
    ListingDetailView,
    AverageRentByCityView,
    AffordabilityView,
    MarketSummaryView,
    RegisterView,
)

urlpatterns = [
    path('listings/', ListingListView.as_view(), name='listing-list'),
    path('listings/<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
    path('analytics/average-rent/', AverageRentByCityView.as_view(), name='average-rent'),
    path('analytics/affordability/', AffordabilityView.as_view(), name='affordability'),
    path('analytics/summary/', MarketSummaryView.as_view(), name='market-summary'),
    path('register/', RegisterView.as_view(), name='register'),
]