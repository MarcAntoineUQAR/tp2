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
        responses={200: AppointmentSerializer},
        operation_summary="Get Appointment By ID",
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
        responses={200: AppointmentSerializer},
        operation_summary="Update Appointment",
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
        responses={200: AppointmentSerializer},
        operation_summary="Partial Update Appointment",
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
        responses={204: 'No Content'},
        operation_summary="Delete Appointment",
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
        operation_summary="Create Appointment",
    )
    def post(self, request, format=None):
        data = request.data
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppointmentList(APIView):
    @swagger_auto_schema(
        tags=['Appointment'], 
        responses={200: AppointmentSerializer(many=True)},
        operation_summary="Get All Appointments",
        )
    def get(self, request, format=None):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)