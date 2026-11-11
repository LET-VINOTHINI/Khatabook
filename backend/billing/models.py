from django.db import models
from business.models import Business
from customers.models import Customer


class Bill(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='bills')
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL, related_name='bills')
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def subtotal(self):
        return sum(item.qty * item.price for item in self.items.all())

    @property
    def tax_amount(self):
        return round(self.subtotal * self.gst_percent / 100, 2)

    @property
    def total(self):
        return self.subtotal + self.tax_amount

    def __str__(self):
        return f'Bill #{self.id} - {self.business.name}'


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    inventory_item = models.ForeignKey(
        'inventory.InventoryItem', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='bill_items'
    )
    name = models.CharField(max_length=150)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.name} x{self.qty}'
