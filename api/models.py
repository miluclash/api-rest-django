# accounts/models.py
import secrets
from django.db import models
from django.contrib.auth.models import User

class UserAPIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="api_key")
    key = models.CharField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(32)  # 64 chars
        super().save(*args, **kwargs)
