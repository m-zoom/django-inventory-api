from rest_framework import serializers
from .models import InventoryItem, InventoryTransaction
from products.serializers import ProductSerializer

class InventoryTransactionSerializer(serializers.ModelSerializer):
    """Serializer for the InventoryTransaction model"""
    inventory_item_name = serializers.ReadOnlyField(source='inventory_item.product.name')
    
    class Meta:
        model = InventoryTransaction
        fields = ['id', 'inventory_item', 'inventory_item_name', 'quantity', 'transaction_type', 'timestamp', 'notes']
        read_only_fields = ['id', 'timestamp']

class InventoryItemSerializer(serializers.ModelSerializer):
    """Serializer for the InventoryItem model"""
    product_details = ProductSerializer(source='product', read_only=True)
    product_name = serializers.ReadOnlyField(source='product.name')
    supplier_name = serializers.ReadOnlyField(source='product.supplier.name')
    low_stock = serializers.BooleanField(source='is_low_stock', read_only=True)
    
    class Meta:
        model = InventoryItem
        fields = ['id', 'product', 'product_name', 'product_details', 'supplier_name', 'quantity', 
                  'low_stock_threshold', 'low_stock', 'last_updated']
        read_only_fields = ['id', 'last_updated', 'low_stock']

class InventoryUpdateSerializer(serializers.Serializer):
    """Serializer for updating inventory levels"""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    transaction_type = serializers.ChoiceField(
        choices=InventoryTransaction.TRANSACTION_TYPES,
        default='adjustment'
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_product_id(self, value):
        """Validate that the product exists"""
        from products.models import Product
        
        try:
            Product.objects.get(pk=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist")
        return value
    
    def create(self, validated_data):
        """Create or update an inventory item and record the transaction"""
        from products.models import Product
        
        product_id = validated_data.get('product_id')
        quantity = validated_data.get('quantity')
        transaction_type = validated_data.get('transaction_type')
        notes = validated_data.get('notes', '')
        
        product = Product.objects.get(pk=product_id)
        
        # Get or create inventory item
        inventory_item, created = InventoryItem.objects.get_or_create(
            product=product,
            defaults={'quantity': 0}
        )
        
        # Update quantity based on transaction type
        if transaction_type == 'addition':
            inventory_item.quantity += quantity
        elif transaction_type == 'reduction':
            if inventory_item.quantity < quantity:
                raise serializers.ValidationError("Not enough items in inventory")
            inventory_item.quantity -= quantity
        else:  # adjustment
            inventory_item.quantity = quantity
        
        inventory_item.save()
        
        # Create transaction record
        transaction_quantity = quantity
        if transaction_type == 'reduction':
            transaction_quantity = -quantity
        
        transaction = InventoryTransaction.objects.create(
            inventory_item=inventory_item,
            quantity=transaction_quantity,
            transaction_type=transaction_type,
            notes=notes
        )
        
        return {
            'inventory_item': inventory_item,
            'transaction': transaction
        }