import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Event(models.Model):
    name = models.CharField(max_length=255)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=30.00)  
    is_active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name="events")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.name} - {self.code}"
