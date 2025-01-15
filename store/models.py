from django.db import models
from django.contrib.auth.models import User

# Model untuk Product
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    
    def __str__(self):
        return self.name

# Model untuk CartItem
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class Transaction(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('bank', 'Bank Transfer'),
        ('digital_wallet', 'Dompet Digital'),
    ]
    BANK_CHOICES = [
        ('bca', 'ATM BCA'),
        ('bri', 'ATM BRI'),
        ('mandiri', 'ATM Mandiri'),
        ('bni', 'ATM BNI'),
    ]
    EWALLET_CHOICES = [
        ('dana', 'Dana'),
        ('gopay', 'Gopay'),
        ('ovo', 'OVO'),
        ('linkaja', 'LinkAja'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')

    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    bank_choice = models.CharField(max_length=50, choices=BANK_CHOICES, null=True, blank=True)
    ewallet_choice = models.CharField(max_length=50, choices=EWALLET_CHOICES, null=True, blank=True)
    payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.user.username} - {self.status}"
