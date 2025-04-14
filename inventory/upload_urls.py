from django.urls import path
from .views import InventoryFileUploadView

# URL patterns for file uploads in the inventory app
urlpatterns = [
    path('inventory-file/', InventoryFileUploadView.as_view(), name='inventory-file-upload'),
]