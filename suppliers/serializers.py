from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for the Supplier model"""
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_name', 'email', 'phone', 'address', 'product_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'product_count']
    
    def get_product_count(self, obj):
        """Get the number of products associated with this supplier"""
        return obj.products.count()