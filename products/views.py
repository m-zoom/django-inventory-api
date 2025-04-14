from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Product CRUD operations
    
    list: GET /api/products/
    retrieve: GET /api/products/{id}/
    create: POST /api/products/
    update: PUT /api/products/{id}/
    partial_update: PATCH /api/products/{id}/
    destroy: DELETE /api/products/{id}/
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'sku', 'supplier']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['name']
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if product has inventory items before deleting
        if hasattr(instance, 'inventory_items') and instance.inventory_items.exists():
            return Response(
                {"detail": "Cannot delete product with existing inventory items."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)