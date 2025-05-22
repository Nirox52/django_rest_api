from rest_framework import generics
from rest_framework.views import APIView
from django.http import Http404
from django.http import JsonResponse
from rest_framework.response import Response
from .models import Incident
from .serializers import IncidentSerializer, IncidentGeoJSONSerializer

class IncidentListCreateView(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

class IncidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

class ActiveIncidentsMapView(APIView):
    def get(self, request):
        active_incidents = Incident.objects.filter(status='active')
        serializer = IncidentGeoJSONSerializer()
        geojson_data = serializer.serialize(
            active_incidents,
            geometry_field='location',
            properties=('id', 'title', 'status', 'created_at')
        )
        return JsonResponse(geojson_data, safe=False)

from django.http import Http404

class IncidentGeoJSONDetailView(APIView):
    """Возвращает конкретный инцидент по ID в формате GeoJSON"""
    def get_object(self, pk):
        try:
            return Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        incident = self.get_object(pk)
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    float(incident.location.x),
                    float(incident.location.y)
                ]
            },
            "properties": {
                "id": incident.id,
                "title": incident.title,
                "status": incident.status,
                "created_at": incident.created_at.isoformat(),
            }
        }
        return Response(feature)
