from django.urls import path, re_path, include
from .views import IncidentListCreateView, IncidentDetailView,ActiveIncidentsMapView,IncidentGeoJSONDetailView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка схемы
schema_view = get_schema_view(
    openapi.Info(
        title="Incidents API",
        default_version='v1',
        description="Документация для API инцидентов",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('incidents/', IncidentListCreateView.as_view(), name='incident-list'),
    path('incidents/<int:pk>/', IncidentDetailView.as_view(), name='incident-detail'),
    path('incidents/geojson/', ActiveIncidentsMapView.as_view(), name='incidents-geojson'),
    path('incidents/geojson/<int:pk>/', IncidentGeoJSONDetailView.as_view(), name='incidents-geojson-detail'),
 
    # Документация
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
