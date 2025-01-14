from django.urls import path
from .views import UserListView, UserUpdateView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),
]
