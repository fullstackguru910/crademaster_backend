from django.urls import path
from .views import (
    FeeListView, FeeUpdateView, RoayltyFeeListView, RoyaltyFeeUpdateView
)

urlpatterns = [
    path('', FeeListView.as_view(), name='fee_list'),
    path('<int:pk>/edit/', FeeUpdateView.as_view(), name='fee_update'),
    path('royalty/', RoayltyFeeListView.as_view(), name='royalty_fee_list'),
    path('royalty/<int:pk>/edit/', RoyaltyFeeUpdateView.as_view(), name='royalty_fee_update'),
]
