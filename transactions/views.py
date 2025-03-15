import time
from decimal import Decimal, ROUND_HALF_UP

from django.views.generic import (
    ListView, DetailView, DeleteView, UpdateView
)
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.timezone import localtime, now
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import StaffRequiredMixin

from fees.models import RoyaltyFee

from .models import Transaction
from .serializers import DepositSerializer, WithdrawSerializer
from .handler import TronTransaction

tron = TronTransaction()
User = get_user_model()


class DepositListView(StaffRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/deposit_list.html'
    context_object_name = 'deposits'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(transaction_type='DEPOSIT')


class DepositDetailView(StaffRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transactions/deposit_detail.html'
    context_object_name = 'deposit'


class DepositUserListView(StaffRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/deposit_list.html'
    context_object_name = 'deposits'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(transaction_type='DEPOSIT', user__pk=self.kwargs.get("pk"))


class WithdrawListView(StaffRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/withdraw_list.html'
    context_object_name = 'withdraws'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(transaction_type='WITHDRAWAL')
    

class WithdrawUserListView(StaffRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/withdraw_list.html'
    context_object_name = 'withdraws'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(transaction_type='WITHDRAWAL', user__pk=self.kwargs.get("pk"))


class WithdrawDetailView(StaffRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transactions/withdraw_detail.html'
    context_object_name = 'withdraw'


class WithdrawDeleteView(StaffRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/withdraw_confirm_delete.html'
    success_url = reverse_lazy('withdraw_list')


class WithdrawApproveView(StaffRequiredMixin, UpdateView):
    model = Transaction
    fields = []
    template_name = 'transactions/withdraw_approve.html'
    context_object_name = 'withdraw'
    success_url = reverse_lazy('withdraw_list')

    def get_object(self):
        return Transaction.objects.get(id=self.kwargs['pk'])

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.status = 'COMPLETED'
        admin = User.objects.get(email='admin@admin.com')

        tx = tron.transfer_usdt(
            admin.cm_wallet,
            admin.cm_private_key,
            instance.address,
            instance.amount
        )
        instance.completed_at = localtime(now())
        instance.status = 'COMPLETED'
        instance.description = tx.get('txid')

        if instance.royalty:
            royalty_fee = RoyaltyFee.get_fee_for_balance(instance.user.get_deposit_balance)
            royalty_amount = (instance.amount * royalty_fee.fee_percentage / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            deposit_data = {
                'user': instance.royalty.pk,
                'amount': royalty_amount,
                'transaction_type': 'ROYALTY',
                'status': 'COMPLETED'
            }
            deposit_serializer = DepositSerializer(data=deposit_data)
            deposit_serializer.is_valid(raise_exception=True)
            deposit_serializer.save()
        instance.save()

        return super().form_valid(form)


class TakeOutDetailView(TemplateView):
    template_name = 'transactions/take_out.html'

    def get_context_data(self, **kwargs):
        user_id = self.kwargs.get('pk')

        user = get_object_or_404(User, id=user_id)
        context = super().get_context_data(**kwargs)
        context['user'] = user
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        admin = User.objects.get(email='admin@admin.com')
        if admin.get_tron_balance < 30:
            return redirect('user_list')
        user = context.get('user')
        amount = user.get_usdt_balance
        # transfer usdt to admin
        txn = tron.transfer_tron(
                admin.cm_wallet,
                admin.cm_private_key,
                user.cm_wallet,
                settings.WITHDRAW_REQUIRED_TRON_AMOUNT
        )
        time.sleep(10)
        txnUSDT = tron.transfer_usdt(
            user.cm_wallet,
            user.cm_private_key,
            admin.cm_wallet,
            amount
        )
        # create deposit
        deposit_data = {
            'user': user.pk,
            'amount': amount,
            'transaction_type': 'DEPOSIT',
            'status': 'COMPLETED'
        }
        deposit_serializer = DepositSerializer(data=deposit_data)
        deposit_serializer.is_valid(raise_exception=True)
        deposit_serializer.save()

        return redirect('user_list')


def check_withdrawal_notification(request):
    cache.set(f"withdrawal_pending", True, timeout=60)
    notify = cache.get(f"withdrawal_pending", False)
    if notify:
        cache.delete(f"withdrawal_pending")
    return JsonResponse({'notify': notify})


# API views

# class DepositCreateAPIView(generics.CreateAPIView):
#     serializer_class = DepositSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         try:
#             user = self.request.user
#             serializer.save(user=user, transaction_type='Deposit')
#         except Exception as e:
#             raise ValidationError(f"Transaction failed: {str(e)}")


class WithdrawCreateAPIView(generics.CreateAPIView):
    serializer_class = WithdrawSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        admin = User.objects.get(email='admin@admin.com')
        txn = tron.transfer_tron(
                user.cm_wallet,
                user.cm_private_key,
                admin.cm_wallet,
                settings.WITHDRAW_REQUIRED_TRON_AMOUNT
        )
        serializer.save(user=user, transaction_type='WITHDRAWAL')
