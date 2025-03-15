from django.urls import path
from .views import (
    DepositListView,
    DepositDetailView,
    DepositUserListView,
    WithdrawListView,
    WithdrawUserListView,
    WithdrawDetailView,
    WithdrawDeleteView,
    WithdrawApproveView,
    TakeOutDetailView,
    check_withdrawal_notification,
)

urlpatterns = [
    path('deposit/', DepositListView.as_view(), name="deposit_list"),
    path('deposit/<int:pk>/', DepositDetailView.as_view(), name="deposit_detail"),
    path('deposit/user/<int:pk>/', DepositUserListView.as_view(), name="deposit_user_list"),

    path('withdraw/', WithdrawListView.as_view(), name="withdraw_list"),
    path('withdraw/user/<int:pk>/', WithdrawUserListView.as_view(), name="withdraw_user_list"),
    path('withdraw/<int:pk>/', WithdrawDetailView.as_view(), name="withdraw_detail"),
    path('withdraw/<int:pk>/approve/', WithdrawApproveView.as_view(), name="withdraw_approve"),
    path('withdraw/<int:pk>/delete/', WithdrawDeleteView.as_view(), name='withdraw_delete'),

    path('take-out/user/<int:pk>/', TakeOutDetailView.as_view(), name="take_out_detail"),
    path('check-withdrawal-notification/', check_withdrawal_notification, name='check_withdrawal_notification'),
]
