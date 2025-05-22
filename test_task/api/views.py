from rest_framework import generics
from rest_framework.views import APIView
from django.http import JsonResponse
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
