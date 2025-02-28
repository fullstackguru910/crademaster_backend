import math
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.utils.timezone import localtime, now
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

from fees.models import Fee
from fees.serializers import FeeSerializer

from transactions.handler import TronTransaction

tron = TronTransaction()


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    wallet = models.CharField(_("wallet address"), max_length=150, blank=True)
    key = models.CharField(_("private key"), max_length=500, blank=True)

    cm_wallet = models.CharField(_("cm wallet address"), max_length=150, blank=True)
    cm_private_key = models.CharField(_("cm private key"), max_length=500, blank=True)
    cm_public_key = models.CharField(_("cm public key"), max_length=500, blank=True)
    cm_hex_address = models.CharField(_("cm hex address"), max_length=150, blank=True)

    profit_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.2)

    referral_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def get_balance(self):
        return self.get_deposit_balance + self.get_royalty_balance + self.get_profits

    @property
    def get_profits(self):
        total_profits = 0
        executes = self.execute_set.all().order_by('created')
        for execute in executes:
            total_profits += execute.get_profit()
        return float(total_profits)

    @property
    def get_deposit_balance(self):
        total_deposit = self.transactions.filter(
            transaction_type='DEPOSIT',
            status='COMPLETED'
        ).aggregate(total_deposit_amount=Sum('amount'))

        total_amount = total_deposit['total_deposit_amount'] or 0
        usdt_balance = self.get_usdt_balance
        event = self.events.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return float(total_amount) + float(usdt_balance) - float(self.get_withdrawal_balance) + float(event)

    @property
    def get_royalty_balance(self):
        total_royalty = self.transactions.filter(
            transaction_type='ROYALTY',
        ).aggregate(total_roaylty_amount=Sum('amount'))

        return total_royalty['total_roaylty_amount'] or 0

    @property
    def get_withdrawal_balance(self):
        total_withdraw = self.transactions.filter(
            transaction_type='WITHDRAWAL',
            status='COMPLETED'
        ).aggregate(total_withdraw_amount=Sum('amount'))

        return total_withdraw['total_withdraw_amount'] or 0

    @property
    def get_tron_balance(self):
        return tron.get_tron_balance(self.cm_wallet)

    @property
    def get_usdt_balance(self):
        return tron.get_usdt_balance(self.cm_wallet)

    @property
    def availability(self):
        balance = self.get_balance
        try:
            fee = Fee.get_fee_for_balance(balance)
            if fee:
                serializer = FeeSerializer(fee)
                return serializer.data
            return FeeSerializer(None).data
        except Exception:
            return FeeSerializer(None).data

    def calculate_total_execute(self):
        total_duration = 0
        executes = self.execute_set.all().order_by('created')

        for execute in executes:
            total_duration += execute.get_duration()
        return math.ceil(total_duration)

    def calculate_elapsed(self):
        execute = self.execute_set.first()

        if not execute or localtime(execute.created).date() != localtime(now()).date():
            return 0
        elapsed = (localtime(now()) - localtime(execute.created)).total_seconds()
        return min(elapsed, 3600 * self.availability.get("hours"))


class IDFile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    front = models.FileField(upload_to='uploads/')
    back = models.FileField(upload_to='uploads/')
    created = models.DateTimeField(auto_now_add=True)
