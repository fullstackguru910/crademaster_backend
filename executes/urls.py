from django.urls import path
from .views import ExecuteListView

urlpatterns = [
    path('<int:pk>/', ExecuteListView.as_view(), name='execute_list'),
]
