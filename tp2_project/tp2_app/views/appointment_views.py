from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from ..models import Appointment
from ..serializers import AppointmentSerializer


class AppointmentDetail(APIView):
    @swagger_auto_schema(
        tags=['Appointment'],
        responses={200: AppointmentSerializer, 404: "Appointment not found"},
        operation_summary="Get appointment details",
        operation_description="Fetch appointment details by ID. Returns 404 if not found."
    )
    def get(self, request, pk, format=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Appointment'],
        request_body=AppointmentSerializer,
        responses={200: AppointmentSerializer, 400: "Invalid data", 404: "Appointment not found"},
        operation_summary="Update an existing appointment",
        operation_description="Update an appointment. 404 if not found."
    )
    def put(self, request, pk, format=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Appointment'],
        request_body=AppointmentSerializer,
        responses={200: AppointmentSerializer, 400: "Invalid data", 404: "Appointment not found"},
        operation_summary="Partially update an appointment",
        operation_description="Update selected fields of an appointment. 404 if not found."
    )
    def patch(self, request, pk, format=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Appointment'], 
        responses={204: "No Content", 404: "Appointment not found"},
        operation_summary="Delete an appointment",
        operation_description="Delete an appointment by ID. 404 if not found."
    )
    def delete(self, request, pk, format=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AppointmentCreate(APIView):
    @swagger_auto_schema(
        tags=['Appointment'],
        request_body=AppointmentSerializer,
        responses={201: AppointmentSerializer, 400: "Invalid data"},
        operation_summary="Create a new appointment",
        operation_description="Create an appointment. Provide all required fields."
    )
    def post(self, request, format=None):
        data = request.data
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentList(APIView):
    @swagger_auto_schema(
        tags=['Appointment'], 
        responses={200: AppointmentSerializer(many=True)},
        operation_summary="Get all appointments",
        operation_description="Retrieve a list of all appointments."
    )
    def get(self, request, format=None):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
