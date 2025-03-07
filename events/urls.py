from django.urls import path
from .views import (
    EventListView,
    EventCreateView,
    EventUpdateView,
    UserEventListView,
    RemoveUserFromEventView,
)

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/edit/', EventUpdateView.as_view(), name='event_update'),
    path('user/<int:pk>/', UserEventListView.as_view(), name='user_event_list'),
    path('<int:event_id>/user/<int:user_id>/remove/', RemoveUserFromEventView.as_view(), name='remove_user_from_event'),
]
