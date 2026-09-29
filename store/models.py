import secrets
import string

from django.conf import settings
from django.db import models


def make_order_reference():
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(8))


class Product(models.Model):
    CATEGORIES = [
        ('Home', 'Home'),
        ('Desk', 'Desk'),
        ('Travel', 'Travel'),
        ('Wear', 'Wear'),
    ]

    name = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(max_length=500)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUSES = [
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    reference = models.CharField(max_length=10, unique=True, default=make_order_reference)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='store_orders')
    full_name = models.CharField(max_length=140)
    email = models.EmailField()
    shipping_address = models.CharField(max_length=240)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUSES, default='Processing')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.reference

    @property
    def total(self):
        return sum((item.unit_price * item.quantity for item in self.items.all()), start=0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=140)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} × {self.product_name}'