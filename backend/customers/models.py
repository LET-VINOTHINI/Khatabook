from django.db import models
from business.models import Business


class Customer(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=120)
    mobile = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class LedgerEntry(models.Model):
    TYPE_CHOICES = [('given', 'Given'), ('received', 'Received')]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='entries')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.customer.name} - {self.type} {self.amount}'
