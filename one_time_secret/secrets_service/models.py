from django.db import models
from django.utils import timezone
from datetime import timedelta

class Secret(models.Model):
    DoesNotExist = None
    secret_key = models.CharField(max_length=64, unique=True)
    secret = models.TextField()
    passphrase = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=1))

    def is_expired(self):
        return timezone.now()   > self.expires_at

    def __str__(self):
        return f'Secret {self.secret_key} ({'expired' if self.is_expired() else 'active'})'