from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from allauth.socialaccount.models import EmailAddress

User = get_user_model()

class EmailVerificationCode(models.Model):
    email_address = models.OneToOneField(
        EmailAddress,
        verbose_name=_("email address"),
        on_delete=models.CASCADE,
        related_name="verification_code",
    )

    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=1)

    def __str__(self):
        return f"{self.email_address.email} - {self.code}"
