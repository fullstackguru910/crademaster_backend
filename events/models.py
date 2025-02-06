from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=30.00)  
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.code}"
