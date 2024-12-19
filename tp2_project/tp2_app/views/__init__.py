from .client_views import ClientList, ClientCreate
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from ..models import Client, Mechanic, Vehicle, Appointment, Bill
from ..serializers import ClientSerializer, MechanicSerializer, VehicleSerializer, AppointmentSerializer, BillSerializer


