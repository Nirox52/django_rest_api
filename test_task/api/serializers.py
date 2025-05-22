from rest_framework import serializers
from djgeojson.serializers import Serializer as GeoJSONSerializer
from .models import Incident

class IncidentGeoJSONSerializer(GeoJSONSerializer):
    class Meta:
        geo_field = 'location'
        properties = ['id', 'title', 'status', 'created_at']

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'
