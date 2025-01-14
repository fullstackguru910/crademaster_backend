from django.urls import path
from .views import (
    DepositListView,
    DepositDetailView,
    DepositApproveView,
    WithdrawListView,
    WithdrawDetailView,
    WithdrawDeleteView,
    WithdrawApproveView,
)

urlpatterns = [
    path('deposit/', DepositListView.as_view(), name="deposit_list"),
    path('deposit/<int:pk>/', DepositDetailView.as_view(), name="deposit_detail"),
    path('deposit/<int:pk>/approve/', DepositApproveView.as_view(), name="deposit_approve"),

    path('withdraw/', WithdrawListView.as_view(), name="withdraw_list"),
    path('withdraw/<int:pk>/', WithdrawDetailView.as_view(), name="withdraw_detail"),
    path('withdraw/<int:pk>/approve/', WithdrawApproveView.as_view(), name="withdraw_approve"),
    path('withdraw/<int:pk>/delete/', WithdrawDeleteView.as_view(), name='withdraw_delete'),
]
