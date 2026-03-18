from django.urls import path
from .views import ListingListView, ListingDetailView

urlpatterns = [
    path('listings/', ListingListView.as_view(), name='listing-list'),
    path('listings/<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
]