from django.db import models

class Supplier(models.Model):
    """Model for storing supplier information"""
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
    
    def __str__(self):
        return self.name