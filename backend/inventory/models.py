from django.db import models
from business.models import Business


class InventoryItem(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='inventory')
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    qty = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    @property
    def is_low_stock(self):
        return self.qty <= self.low_stock_threshold

    def __str__(self):
        return self.name
