from rest_framework import fields, serializers
from .models import Client, Mechanic, Vehicle, Appointment, Bill

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'username', 'firstname', 'lastname', 'email', 'password', 'phone_number', 'address']

class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mechanic
        fields = ['id', 'username', 'firstname', 'lastname', 'email', 'password', 'salary']

class VehicleSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'client', 'make', 'model', 'year', 'color']

class AppointmentSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    mechanic = MechanicSerializer(read_only=True)
    vehicle = VehicleSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'client', 'mechanic', 'vehicle', 'date', 'description']

class BillSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    appointment = AppointmentSerializer(read_only=True)

    class Meta:
        model = Bill
        fields = ['id', 'client', 'appointment', 'amount', 'date', 'is_paid']
