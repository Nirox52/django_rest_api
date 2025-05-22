from django.urls import path
from .views import IncidentListCreateView, IncidentDetailView,ActiveIncidentsMapView,IncidentGeoJSONDetailView

urlpatterns = [
    path('incidents/', IncidentListCreateView.as_view(), name='incident-list'),
    path('incidents/<int:pk>/', IncidentDetailView.as_view(), name='incident-detail'),
    path('incidents/geojson/', ActiveIncidentsMapView.as_view(), name='incidents-geojson'),
    path('incidents/geojson/<int:pk>/', IncidentGeoJSONDetailView.as_view(), name='incidents-geojson-detail'),
]
