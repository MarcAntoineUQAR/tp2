from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from ..models import Mechanic
from ..serializers import MechanicSerializer

class MechanicDetail(APIView):
    @swagger_auto_schema(
        tags=['Mechanic'],
        responses={200: MechanicSerializer, 404: "Mechanic not found"},
        operation_summary="Get mechanic details",
        operation_description="Fetch mechanic details by ID. Returns 404 if mechanic not found."
    )
    def get(self, request, pk, format=None):
        try:
            mechanic = Mechanic.objects.get(pk=pk)
        except Mechanic.DoesNotExist:
            return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MechanicSerializer(mechanic)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Mechanic'],
        request_body=MechanicSerializer,
        responses={200: MechanicSerializer, 404: "Mechanic not found", 400: "Invalid data"},
        operation_summary="Update mechanic details",
        operation_description="Update an existing mechanic by ID. Returns 404 if mechanic not found."
    )
    def put(self, request, pk, format=None):
        try:
            mechanic = Mechanic.objects.get(pk=pk)
        except Mechanic.DoesNotExist:
            return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MechanicSerializer(mechanic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Mechanic'],
        request_body=MechanicSerializer,
        responses={200: MechanicSerializer, 404: "Mechanic not found", 400: "Invalid data"},
        operation_summary="Partially update mechanic details",
        operation_description="Partially update mechanic details by ID. Returns 404 if mechanic not found."
    )
    def patch(self, request, pk, format=None):
        try:
            mechanic = Mechanic.objects.get(pk=pk)
        except Mechanic.DoesNotExist:
            return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MechanicSerializer(mechanic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Mechanic'], 
        responses={204: "No Content", 404: "Mechanic not found"},
        operation_summary="Delete mechanic",
        operation_description="Delete a mechanic by ID. Returns 404 if mechanic not found."
    )
    def delete(self, request, pk, format=None):
        try:
            mechanic = Mechanic.objects.get(pk=pk)
        except Mechanic.DoesNotExist:
            return Response({'error': 'Mechanic not found'}, status=status.HTTP_404_NOT_FOUND)
        mechanic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MechanicCreate(APIView):
    @swagger_auto_schema(
        tags=['Mechanic'],
        request_body=MechanicSerializer,
        responses={201: MechanicSerializer, 400: "Invalid data"},
        operation_summary="Create a new mechanic",
        operation_description="Create a new mechanic with the necessary details."
    )
    def post(self, request, format=None):
        data = request.data
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = MechanicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MechanicList(APIView):
    @swagger_auto_schema(
        tags=['Mechanic'], 
        responses={200: MechanicSerializer(many=True)},
        operation_summary="Get all mechanics",
        operation_description="Retrieve a list of all mechanics."
    )
    def get(self, request, format=None):
        mechanics = Mechanic.objects.all()
        serializer = MechanicSerializer(mechanics, many=True)
        return Response(serializer.data)
