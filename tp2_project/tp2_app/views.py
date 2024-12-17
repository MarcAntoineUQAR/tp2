from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema  # Import the decorator
from .models import Client, Mechanic, Vehicle, Appointment, Bill
from .serializers import ClientSerializer, MechanicSerializer, VehicleSerializer, AppointmentSerializer, BillSerializer

def home(request):
    return HttpResponse("<html><body><p>home</p></body></html>")

class ClientDetail(APIView):

    @swagger_auto_schema(tags=['Client Group'], responses={200: ClientSerializer})
    def get(self, request, pk, format=None):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Client Group'], responses={200: ClientSerializer})
    def put(self, request, pk, format=None):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['Client Group'], responses={200: ClientSerializer})
    def patch(self, request, pk, format=None):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['Client Group'], responses={204: 'No Content'})
    def delete(self, request, pk, format=None):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientCreate(APIView):

    @swagger_auto_schema(tags=['Client Group'], responses={201: ClientSerializer})
    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)