from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model"""
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'sku', 'supplier', 'supplier_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_sku(self, value):
        """Validate that the SKU is unique"""
        # Check if SKU exists for a different product when updating
        if self.instance and self.instance.sku == value:
            return value
            
        if Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError("A product with this SKU already exists.")
        return value