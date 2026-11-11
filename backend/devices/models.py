from django.conf import settings
from django.db import models


class Device(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=150)
    device_token = models.CharField(max_length=255, blank=True)
    last_active = models.DateTimeField(auto_now=True)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_active']

    def __str__(self):
        return self.name
