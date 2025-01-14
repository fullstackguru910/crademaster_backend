from rest_framework import serializers

from .models import Transaction

class DepositSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'transaction_type', 'status']

    def validate(self, data):
        # user = self.context['request'].user
        return data


class WithdrawSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'address', 'status', 'requested_at', 'completed_at']
        read_only_fields = ['id', 'user', 'status', 'requested_at', 'completed_at']

    def validate(self, data):
        user = self.context['request'].user
        if Transaction.objects.filter(user=user, status='PENDING').exists():
            raise serializers.ValidationError("You already have a pending withdrawal request.")

        if data['amount'] > user.get_balance:
            raise serializers.ValidationError("Exceed amount.")

        if data['address'] == user.cm_address:
            raise serializers.ValidationError("Withdrawal address shouldn't be the crademaster wallet.")
        return data
