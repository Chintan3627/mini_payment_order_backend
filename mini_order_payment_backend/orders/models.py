from django.db import models
from auth_flow.models import CustomUser
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.name} - {self.price}"


class Order(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_PAID = 'PAID'
    STATUS_FAILED = 'FAILED'
    STATUS_CHOICES = [
    (STATUS_PENDING, 'Pending'),
    (STATUS_PAID, 'Paid'),
    (STATUS_FAILED, 'Failed'),
    ]


    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    customer_email = models.EmailField()
    order_id = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)


    # Razorpay related
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)


    # CRM sync status and response
    crm_synced = models.BooleanField(default=False)
    crm_response = models.JSONField(null=True, blank=True)

    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save first so ID is generated

        if is_new:
            self.order_id = f"ORD-{str(self.id).zfill(6)}"
            super().save(update_fields=['order_id'])
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_email} - {self.status}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)


    def get_line_total(self):
     return self.unit_price * self.quantity


    def __str__(self):
        return f"{self.quantity} x {self.product.name} @ {self.unit_price}"