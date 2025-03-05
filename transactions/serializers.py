from tronpy import Tron
from django.db.models import Sum
from django.conf import settings
from rest_framework import serializers

from .models import Transaction

class DepositSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'transaction_type', 'status', 'description', 'completed_at']

    def validate(self, data):
        # user = self.context['request'].user
        return data


class WithdrawSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'address', 'status', 'requested_at', 'completed_at']
        read_only_fields = ['id', 'user', 'status', 'requested_at', 'completed_at']

    def validate_address(self, value):
        """
        Validate the withdrawal address format.
        """
        if not Tron().is_address(value):
            raise serializers.ValidationError("Invalid Tron address.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        if Transaction.objects.filter(user=user, status='PENDING').exists():
            raise serializers.ValidationError("You already have a pending withdrawal request.")

        if data['amount'] > user.get_balance:
            raise serializers.ValidationError("Exceed amount.")
        
        if data['amount'] < 1:
            raise serializers.ValidationError("The minimum withdrawal amount should be 1 USDT.")

        if data['address'] == user.cm_wallet:
            raise serializers.ValidationError("Withdrawal address shouldn't be the crademaster wallet.")\
            
        if user.get_tron_balance < settings.MINIMUM_TRON_AMOUNT:
            raise serializers.ValidationError(f"Your Tron balance is insufficient. Please ensure your balance is greater than {settings.MINIMUM_TRON_AMOUNT} TRX to proceed.")

        invests = user.events.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        if data['amount'] > user.get_balance - float(invests):
            raise serializers.ValidationError("You can not withdraw event amount.")

        return data
