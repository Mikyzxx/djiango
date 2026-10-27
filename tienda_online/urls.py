"""
URL configuration for tienda_online project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Tienda Online API",
        default_version='v1',
        description="Documentación interactiva de la API para la plataforma Tienda Online. Incluye autenticación con JWT, CRUD de usuarios con campo extra de teléfono y catálogo de productos.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contacto@tiendaonline.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('products.urls')),
    path('api/', include('products.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
