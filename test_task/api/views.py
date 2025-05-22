from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from .models import Incident
from .serializers import IncidentSerializer, IncidentGeoJSONSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class IncidentListCreateView(generics.ListCreateAPIView):
    """
    API endpoint для отримання списку інцедентів та їх створення
    """
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    @swagger_auto_schema(
        operation_summary="Список усіх інцедентів",
        operation_description="Отримання списку усіх інцедентів з можєливістю пагінації",
        responses={
            200: IncidentSerializer(many=True),
            400: "Помилкові параметри запиту"
        },
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Фільтр по статусу (active, closed, in_progress)",
                type=openapi.TYPE_STRING,
                enum=['active', 'closed', 'in_progress']
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Кількість елементів на сторінці",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Створити новий інцедент",
        operation_description="Створеня нового інцеденту за локацією та іншими параметрами",
        request_body=IncidentSerializer,
        responses={
            201: IncidentSerializer,
            400: "Невалідні данні"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class IncidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint для отримання та редегування інцеденту
    """
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    @swagger_auto_schema(
        operation_summary="Отримати деталі інцеденту",
        operation_description="Отримання повної інформації про інцедент за id",
        responses={
            200: IncidentSerializer,
            404: "Інцедент не знайдено"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Оновити інцедент",
        operation_description="Оновлення параметрів інцеденту",
        request_body=IncidentSerializer,
        responses={
            200: IncidentSerializer,
            400: "Помилкові данні",
            404: "Інцедент не знайдено"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Видалити інцедент",
        operation_description="Видалення інцеденту з бд",
        responses={
            204: "Інцедент видалено",
            404: "Інцедент не знайдено"
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ActiveIncidentsMapView(APIView):
    """
    API endpoint для отримання активних інцедентів у форматі GeoJSON
    """
    @swagger_auto_schema(
        operation_summary="Активні інцеденти",
        operation_description="Отримання активних інцедентів у форматі GeoJSON",
        responses={
            200: openapi.Response(
                description="GeoJSON FeatureCollection",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['FeatureCollection']),
                        'features': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['Feature']),
                                    'geometry': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['Point']),
                                            'coordinates': openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Items(type=openapi.TYPE_NUMBER),
                                                min_items=2,
                                                max_items=2
                                            )
                                        }
                                    ),
                                    'properties': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                            'title': openapi.Schema(type=openapi.TYPE_STRING),
                                            'status': openapi.Schema(type=openapi.TYPE_STRING),
                                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time')
                                        }
                                    )
                                }
                            )
                        )
                    }
                )
            ),
            500: "Помилка серверу"
        }
    )
    def get(self, request):
        active_incidents = Incident.objects.filter(status='active')
        serializer = IncidentGeoJSONSerializer()
        geojson_data = serializer.serialize(
            active_incidents,
            geometry_field='location',
            properties=('id', 'title', 'status', 'created_at')
        )
        return JsonResponse(geojson_data, safe=False)


class IncidentGeoJSONDetailView(APIView):
    """
    API endpoint для отримання конкретного інцеденту у форматі GeoJSON
    """
    @swagger_auto_schema(
        operation_summary="Деталі інцеденту",
        operation_description="Отримання конкретного інцеденту у форматі GeoJSON",

        responses={
            200: openapi.Response(
                description="GeoJSON Feature",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['Feature']),
                        'geometry': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['Point']),
                                'coordinates': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Items(type=openapi.TYPE_NUMBER),
                                    min_items=2,
                                    max_items=2
                                )
                            }
                        ),
                        'properties': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'title': openapi.Schema(type=openapi.TYPE_STRING),
                                'status': openapi.Schema(type=openapi.TYPE_STRING),
                                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time')
                            }
                        )
                    }
                )
            ),
            404: "Інцедент не знайдено"
        }
    )
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

    def get_object(self, pk):
        try:
            return Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            raise Http404
