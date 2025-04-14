from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework import views as rest_views
from .views import (
    InventoryItemViewSet,
    InventoryTransactionViewSet,
    InventoryUpdateView
)

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'items', InventoryItemViewSet)
router.register(r'transactions', InventoryTransactionViewSet)

# URL patterns for the inventory app
urlpatterns = [
    path('update/', InventoryUpdateView.as_view(), name='inventory-update'),
]

# Add router URLs to urlpatterns
urlpatterns += router.urls