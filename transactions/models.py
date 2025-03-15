from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.dispatch import receiver


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', _('Deposit')),
        ('WITHDRAWAL', _('Withdrawal')),
        ('ROYALTY', _('Royalty')),
    ]
    STATUS_CHOICES = [
        ('PENDING', _('Pending')),
        ('COMPLETED', _('Completed')),
        ('CANCELLED', _('Cancelled')),
        ('FAILED', _('Failed')),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(_("amount"), max_digits=10, decimal_places=2)
    transaction_type = models.CharField(_("transaction type"), max_length=10, choices=TRANSACTION_TYPES)
    status = models.CharField(_("status"), max_length=10, choices=STATUS_CHOICES, default='PENDING')
    requested_at = models.DateTimeField(_("requested at"), auto_now_add=True)
    completed_at = models.DateTimeField(_("completed at"), null=True, blank=True)
    description = models.TextField(_("description"), blank=True, null=True)
    address = models.CharField(_("wallet address"), max_length=150, blank=True, null=True)
    royalty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='royalties', blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} {self.id} - {self.user.email} - {self.status}"

    def save(self, *args, **kwargs):
        if self.transaction_type == 'WITHDRAWAL' and not self.address:
            raise ValueError("Wallet address is required for withdrawals.")
        super().save(*args, **kwargs)


class TronDeposit(models.Model):
    STATUS_CHOICES = [
        ('PENDING', _('Pending')),
        ('COMPLETED', _('Completed')),
        ('CANCELLED', _('Cancelled')),
        ('FAILED', _('Failed')),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tron_deposits')
    amount = models.DecimalField(_("amount"), max_digits=10, decimal_places=2)
    status = models.CharField(_("status"), max_length=10, choices=STATUS_CHOICES, default='PENDING')
    requested_at = models.DateTimeField(_("requested at"), auto_now_add=True)
    completed_at = models.DateTimeField(_("completed at"), null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount}"


@receiver(post_save, sender=Transaction)
def notify_withdrawal_pending(sender, instance, created, **kwargs):
    if created and instance.transaction_type == 'WITHDRAWAL' and instance.status == 'PENDING':
        from django.core.cache import cache
        cache.set(f"withdrawal_pending", True, timeout=60)
