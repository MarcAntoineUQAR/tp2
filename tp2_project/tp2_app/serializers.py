import datetime
from rest_framework import serializers
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
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source='client', write_only=True
    )
    client = serializers.StringRelatedField(read_only=True)
    
    def validate_year(self, value):
        if value < 1000 or value > datetime.now().year:
            raise serializers.ValidationError("L'année doit être comprise entre 1886 et l'année actuelle.")
        return value

    class Meta:
        model = Vehicle
        fields = ['id', 'client', 'client_id', 'make', 'model', 'year', 'color']

class AppointmentSerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source='client', write_only=True
    )
    mechanic_id = serializers.PrimaryKeyRelatedField(
        queryset=Mechanic.objects.all(), source='mechanic', write_only=True
    )
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(), source='vehicle', write_only=True
    )
    client = serializers.StringRelatedField(read_only=True)
    mechanic = serializers.StringRelatedField(read_only=True)
    vehicle = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'client', 'client_id', 'mechanic', 'mechanic_id', 'vehicle', 'vehicle_id', 'date', 'description', 'is_accepted']

class BillSerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source='client', write_only=True
    )
    appointment_id = serializers.PrimaryKeyRelatedField(
        queryset=Appointment.objects.all(), source='appointment', write_only=True
    )
    client = serializers.StringRelatedField(read_only=True)
    appointment = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Bill
        fields = ['id', 'client', 'client_id', 'appointment', 'appointment_id', 'amount', 'date', 'is_paid']
