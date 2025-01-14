from django.urls import path, include

from .views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('fee/', include('fees.urls')),
    path('user/', include('users.urls')),
    path('execute/', include('executes.urls')),
    path('transaction/', include('transactions.urls')),
]
