from django.urls import path
from .views import InventoryReportView

# URL patterns for reports in the inventory app
urlpatterns = [
    path('inventory-summary/', InventoryReportView.as_view(), name='inventory-summary-report'),
]