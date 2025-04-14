from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    """Model for storing product information"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    sku = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Foreign key relationship with Supplier
    supplier = models.ForeignKey(
        'suppliers.Supplier', 
        on_delete=models.CASCADE,
        related_name='products'
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return self.name