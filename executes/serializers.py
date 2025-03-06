from django.utils.timezone import now, localtime
from django.conf import settings
from rest_framework import serializers

from fees.models import Fee
from .models import Execute


class ExecuteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Execute
        fields = ['id', 'user', 'amount', 'duration', 'created']
        read_only_fields = ['id', 'user', 'amount', 'duration', 'created']

    def validate(self, data):
        """
        Validate that the user can create a Execute record only once per day.
        """
        user = self.context['request'].user
        today = localtime(now()).date()

        if user.get_deposit_balance < settings.WITHDRAW_REQUIRED_USDT_AMOUNT:
            raise serializers.ValidationError(f"Your USDT balance is insufficient. Please ensure your balance is greater than {settings.WITHDRAW_REQUIRED_USDT_AMOUNT} USDT to proceed.")
        
        print(user.get_usdt_balance, user.get_tron_balance, settings.MINIMUM_TRON_AMOUNT)

        if user.get_usdt_balance > 0 and user.get_tron_balance < settings.MINIMUM_TRON_AMOUNT:
            raise serializers.ValidationError(f"Your Tron balance is insufficient. Please ensure your balance is greater than {settings.MINIMUM_TRON_AMOUNT} TRX to proceed.")

        if Execute.objects.filter(user=user, created__date=today).exists():
            raise serializers.ValidationError("You can only activate the platform once per day.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        amount = user.get_balance

        applicable_fee = Fee.objects.filter(min_investment__lte=amount, max_investment__gte=amount).first()

        if not applicable_fee:
            raise serializers.ValidationError("No fee found for the given investment amount.")

        execute = Execute.objects.create(duration=applicable_fee.hours, user=user, amount=amount, profit_percent=user.profit_percent)
        return execute
    

class ExecuteHistorySerializer(serializers.ModelSerializer):
    profit = serializers.SerializerMethodField()
    profit_duration = serializers.SerializerMethodField()
    platform_fee_amount = serializers.SerializerMethodField()

    class Meta:
        model = Execute
        fields = ['amount', 'profit', 'platform_fee_amount', 'profit_percent', 'profit_duration', 'created']

    def get_profit(self, obj):
        return obj.get_profit()
    
    def get_platform_fee_amount(self, obj):
        return obj.get_platform_fee_amount()
    
    def get_profit_duration(self, obj):
        return obj.get_duration()
