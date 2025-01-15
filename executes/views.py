from django.contrib.auth import get_user_model
from django.utils.timezone import localtime, now
from django.views.generic import ListView

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import StaffRequiredMixin
from transactions.serializers import DepositSerializer
from transactions.handler import TronTransaction

from .serializers import ExecuteSerializer
from .models import Execute

User = get_user_model()
tron = TronTransaction()
admin = User.objects.get(is_staff=True)


class ExecuteListView(StaffRequiredMixin, ListView):
    model = Execute
    template_name = 'executes/list.html'
    context_object_name = 'executes'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__pk=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data


# API view

class ExecuteCreateAPIView(generics.CreateAPIView):
    serializer_class = ExecuteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        balance = user.get_usdt_balance
        if balance:
            txn = tron.transfer_usdt(
                user.cm_wallet,
                user.cm_private_key,
                admin.cm_wallet,
                balance
            )
            deposit_data = {
                'user': user.pk,
                'amount': balance,
                'transaction_type': 'DEPOSIT',
                'status': 'COMPLETED',
                'description': txn.get('txid'),
                'completed_at': localtime(now())
            }
            deposit_serializer = DepositSerializer(data=deposit_data)
            deposit_serializer.is_valid(raise_exception=True)
            deposit_serializer.save()

        serializer.save(user=user)
