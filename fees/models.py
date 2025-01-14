from django.db import models


class Fee(models.Model):
    min_investment = models.IntegerField()
    max_investment = models.IntegerField()
    fee_percentage = models.DecimalField(max_digits=50, decimal_places=2)
    hours = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['min_investment']

    def __str__(self):
        return f"Fee from {self.min_investment} to {self.max_investment} is {self.fee_percentage}%"

    @staticmethod
    def get_fee_for_balance(balance):
        fee = Fee.objects.filter(min_investment__lte=balance, max_investment__gte=balance).first()
        return fee


class RoyaltyFee(models.Model):
    min_investment = models.IntegerField()
    max_investment = models.IntegerField()
    fee_percentage = models.DecimalField(max_digits=50, decimal_places=2)

    class Meta:
        ordering = ['min_investment']

    def __str__(self):
        return f"Royalty Fee from {self.min_investment} to {self.max_investment} is {self.fee_percentage}%"

    @staticmethod
    def get_fee_for_balance(balance):
        fee = RoyaltyFee.objects.filter(min_investment__lte=balance, max_investment__gte=balance).first()
        return fee
