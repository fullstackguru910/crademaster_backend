import math
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.utils.timezone import localtime, now

from fees.models import RoyaltyFee

User = get_user_model()


class Execute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    duration = models.IntegerField(default=0)
    agent_os = models.CharField(max_length=10, null=True, blank=True)  # OS
    http_user_agent = models.CharField(max_length=40, null=True, blank=True)  # HTTP_USER_AGENT
    http_referer = models.CharField(max_length=40, null=True, blank=True)  # HTTP_REFERER
    http_x_forwarded_for = models.CharField(max_length=100, null=True, blank=True) # HTTP_X_FORWARDED_FOR
    profit_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.2)
    created = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Execute from {self.user.email} is ${self.amount}"
    
    def get_duration(self):
        current_time = localtime(now())
        created_time = localtime(self.created)
        if created_time.date() == current_time.date():
            time_difference = (current_time - created_time).total_seconds()
        else:
            end_of_day = created_time.replace(hour=23, minute=59, second=59)
            time_difference = (end_of_day - created_time).total_seconds()
        return min(time_difference, self.duration * 3600)

    def get_profit(self):
        duration = self.get_duration()
        profit = self.amount * duration / 3600 * float(self.profit_percent) / 100
        return math.ceil(profit - self.get_platform_fee_amount())

    def get_platform_fee(self):
        fee = RoyaltyFee.get_fee_for_balance(self.amount)
        return fee.fee_percentage

    def get_platform_fee_amount(self):
        duration = self.get_duration()
        profit = self.amount * duration / 3600 * float(self.profit_percent) / 100
        return math.ceil(profit * float(self.get_platform_fee()) / 100)
