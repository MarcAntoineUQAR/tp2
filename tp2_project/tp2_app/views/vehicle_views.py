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
        responses={200: VehicleSerializer, 404: "Vehicle not found"},
        operation_summary="Get vehicle details",
        operation_description="Fetch vehicle details by ID. Returns 404 if vehicle not found."
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
        responses={200: VehicleSerializer, 404: "Vehicle not found", 400: "Invalid data"},
        operation_summary="Update vehicle details",
        operation_description="Update an existing vehicle by ID. Returns 404 if vehicle not found."
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
        responses={200: VehicleSerializer, 404: "Vehicle not found", 400: "Invalid data"},
        operation_summary="Partially update vehicle details",
        operation_description="Partially update vehicle details by ID. Returns 404 if vehicle not found."
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
        responses={204: "No Content", 404: "Vehicle not found"},
        operation_summary="Delete vehicle",
        operation_description="Delete a vehicle by ID. Returns 404 if vehicle not found."
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
        operation_summary="Create a new vehicle",
        operation_description="Create a new vehicle with the required details."
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
        operation_summary="Get all vehicles",
        operation_description="Retrieve a list of all vehicles."
    )
    def get(self, request, format=None):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
