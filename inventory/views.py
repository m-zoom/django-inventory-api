from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from django.db.models import F, Sum, Count
from .models import InventoryItem, InventoryTransaction
from .serializers import (
    InventoryItemSerializer,
    InventoryTransactionSerializer,
    InventoryUpdateSerializer
)

class InventoryItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing inventory items
    """
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    
    def get_queryset(self):
        """
        Optionally filter by product or low stock status
        """
        queryset = InventoryItem.objects.all()
        
        # Filter by product ID if provided
        product_id = self.request.query_params.get('product_id', None)
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        
        # Filter by low stock status if provided
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock is not None and low_stock.lower() == 'true':
            queryset = queryset.filter(quantity__lte=F('low_stock_threshold'))
        
        return queryset

class InventoryTransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing inventory transactions
    """
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer
    
    def get_queryset(self):
        """
        Optionally filter by inventory item
        """
        queryset = InventoryTransaction.objects.all()
        
        # Filter by inventory item ID if provided
        item_id = self.request.query_params.get('item_id', None)
        if item_id is not None:
            queryset = queryset.filter(inventory_item_id=item_id)
        
        return queryset

class InventoryUpdateView(generics.CreateAPIView):
    """
    API view for updating inventory levels
    """
    serializer_class = InventoryUpdateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create or update inventory item and record transaction
        result = serializer.save()
        
        return Response(
            {"message": "Inventory updated successfully", "data": result},
            status=status.HTTP_200_OK
        )


class InventoryFileUploadView(generics.CreateAPIView):
    """
    API view for uploading inventory files (CSV, Excel, etc.)
    """
    parser_classes = (MultiPartParser, FormParser)
    
    def create(self, request, *args, **kwargs):
        file_obj = request.data.get('file')
        
        if not file_obj:
            return Response(
                {"error": "No file provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read CSV file
            import csv
            from io import TextIOWrapper
            
            csv_file = TextIOWrapper(file_obj.file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
            
            # Validate required fields
            required_fields = ['product_id', 'name', 'quantity', 'price']
            if not all(field in reader.fieldnames for field in required_fields):
                return Response(
                    {"error": f"CSV must contain these fields: {', '.join(required_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Process each row and save to database
            created_count = 0
            for row in reader:
                # Create or update inventory item
                InventoryItem.objects.update_or_create(
                    product_id=row['product_id'],
                    defaults={
                        'name': row['name'],
                        'quantity': row['quantity'],
                        'price': row['price'],
                    }
                )
                created_count += 1
            
            return Response(
                {"message": f"Successfully processed {created_count} products"},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"error": f"Error processing file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class InventoryReportView(generics.RetrieveAPIView):
    """
    API view for generating inventory reports
    """
    
    def retrieve(self, request, *args, **kwargs):
        # Get summary statistics
        total_items = InventoryItem.objects.count()
        total_quantity = InventoryItem.objects.aggregate(total=Sum('quantity'))['total'] or 0
        low_stock_count = InventoryItem.objects.filter(quantity__lte=F('low_stock_threshold')).count()
        
        # Get recent transactions
        recent_transactions = InventoryTransaction.objects.order_by('-timestamp')[:5]
        recent_transaction_data = InventoryTransactionSerializer(recent_transactions, many=True).data
        
        return Response({
            "summary": {
                "total_items": total_items,
                "total_quantity": total_quantity,
                "low_stock_count": low_stock_count,
            },
            "recent_transactions": recent_transaction_data
        })