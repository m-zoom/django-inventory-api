from django.db import models
from django.core.validators import MinValueValidator
from products.models import Product

class InventoryItem(models.Model):
    """Model for tracking inventory levels of products"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='inventory_items'
    )
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Threshold for low stock alerts
    low_stock_threshold = models.PositiveIntegerField(
        default=10,
        help_text="Quantity threshold for low stock alerts"
    )
    
    class Meta:
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'
        ordering = ['product__name']
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} in stock"
    
    @property
    def is_low_stock(self):
        """Check if the inventory level is below the threshold"""
        return self.quantity <= self.low_stock_threshold

class InventoryTransaction(models.Model):
    """Model for tracking inventory transactions"""
    TRANSACTION_TYPES = (
        ('addition', 'Addition'),
        ('reduction', 'Reduction'),
        ('adjustment', 'Adjustment'),
    )
    
    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    quantity = models.IntegerField(
        help_text="Positive for additions, negative for reductions"
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Inventory Transaction'
        verbose_name_plural = 'Inventory Transactions'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.transaction_type} of {abs(self.quantity)} units for {self.inventory_item.product.name}"