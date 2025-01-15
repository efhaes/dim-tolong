from django.contrib import admin
from .models import Product, CartItem, Transaction

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Transaction)
