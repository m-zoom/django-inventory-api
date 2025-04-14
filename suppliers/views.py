from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Supplier
from .serializers import SupplierSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Supplier CRUD operations
    
    list: GET /api/suppliers/
    retrieve: GET /api/suppliers/{id}/
    create: POST /api/suppliers/
    update: PUT /api/suppliers/{id}/
    partial_update: PATCH /api/suppliers/{id}/
    destroy: DELETE /api/suppliers/{id}/
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'contact_name']
    search_fields = ['name', 'contact_name', 'email', 'phone', 'address']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']