from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Create schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Inventory Management System API",
        default_version='v1',
        description="A RESTful API for managing inventory, products, and suppliers",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API endpoints
    path('api/', include([
        path('products/', include('products.urls')),
        path('suppliers/', include('suppliers.urls')),
        path('inventory/', include('inventory.urls')),
        path('upload/', include('inventory.upload_urls')),
        path('reports/', include('inventory.report_urls')),
    ])),
    # API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)