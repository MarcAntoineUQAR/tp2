from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from ..models import Client
from ..serializers import ClientSerializer

class ClientDetail(APIView):
    @swagger_auto_schema(
        tags=['Client'],
        responses={200: ClientSerializer},
        operation_summary="Get Client By ID",
        )
    def get(self, request, pk, format=None):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Client'],
        request_body=ClientSerializer,
        responses={200: ClientSerializer},
        operation_summary="Update Client",
        )
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

    @swagger_auto_schema(
        tags=['Client'],
        request_body=ClientSerializer,
        responses={200: ClientSerializer},
        operation_summary="Partial Update Client",
        )
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

    @swagger_auto_schema(
        tags=['Client'], 
        responses={204: 'No Content'},
        operation_summary="Delete Client",
        )
    def delete(self, request, pk, format=None):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ClientCreate(APIView):
    @swagger_auto_schema(
        tags=['Client'],
        request_body=ClientSerializer,
        responses={201: ClientSerializer, 400: "Invalid data"},
        operation_summary="Create Client",
    )
    def post(self, request, format=None):
        data = request.data
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientList(APIView):
    @swagger_auto_schema(
        tags=['Client'], 
        responses={200: ClientSerializer(many=True)},
        operation_summary="Get All Clients",
        )
    def get(self, request, format=None):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)