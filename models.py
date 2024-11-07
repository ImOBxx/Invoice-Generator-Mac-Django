from django.db import models
from django.utils import timezone 

class Invoice(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    product_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateTimeField(auto_now_add=True)
    date_created = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        # Set total_amount to grand_total before saving
        self.total_amount = self.grand_total
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"Invoice for {self.name}"
