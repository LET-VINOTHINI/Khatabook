from django.conf import settings
from django.db import models


class Business(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=100, blank=True)
    upi_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name


class BusinessMembership(models.Model):
    ROLE_CHOICES = [('owner', 'Owner'), ('staff', 'Staff')]

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='memberships'
    )
    name = models.CharField(max_length=120)
    mobile = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')
    can_add_entries = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-role', 'created_at']
        unique_together = ('business', 'mobile')

    def __str__(self):
        return f'{self.name} @ {self.business.name}'
