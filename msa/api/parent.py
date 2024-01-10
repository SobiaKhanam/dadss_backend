import json

from django_filters.rest_framework import DjangoFilterBackend
from postgis import Geometry
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import authentication_classes, action
from rest_framework import viewsets, status, serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response


class SessionCsrfExemptAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


class PositionField(serializers.JSONField):
    def to_representation(self, value):
        if self.binary:
            value = json.dumps(value, cls=self.encoder)
            value = value.encode()
        if isinstance(value, str):
            return (Geometry.from_ewkb(value)).geojson
        return value


@authentication_classes([SessionCsrfExemptAuthentication])
class CustomViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    @action(methods=['get'], detail=False)
    def count(self, request):
        return Response({'count': self.queryset.count()})
