from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from ..models import Vehicle
from ..serializers import VehicleSerializer

class VehicleDetail(APIView):
    @swagger_auto_schema(
        tags=['Vehicle'],
        responses={200: VehicleSerializer},
        operation_summary="Get Vehicle By ID",
        )
    def get(self, request, pk, format=None):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Vehicle'],
        request_body=VehicleSerializer,
        responses={200: VehicleSerializer},
        operation_summary="Update Vehicle",
        )
    def put(self, request, pk, format=None):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Vehicle'],
        request_body=VehicleSerializer,
        responses={200: VehicleSerializer},
        operation_summary="Partial Update Vehicle",
        )
    def patch(self, request, pk, format=None):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Vehicle'], 
        responses={204: 'No Content'},
        operation_summary="Delete Vehicle",
        )
    def delete(self, request, pk, format=None):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VehicleCreate(APIView):
    @swagger_auto_schema(
        tags=['Vehicle'],
        request_body=VehicleSerializer,
        responses={201: VehicleSerializer, 400: "Invalid data"},
        operation_summary="Create Vehicle",
    )
    def post(self, request, format=None):
        data = request.data
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VehicleList(APIView):
    @swagger_auto_schema(
        tags=['Vehicle'], 
        responses={200: VehicleSerializer(many=True)},
        operation_summary="Get All Vehicles",
        )
    def get(self, request, format=None):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)