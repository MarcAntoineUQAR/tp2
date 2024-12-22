from django.shortcuts import render
from rest_framework.test import APIRequestFactory
from tp2_app.models import Client, Mechanic, Appointment, Vehicle, Bill
from tp2_app.views import ClientList
from tp2_app.views.bill_views import BillList
from tp2_app.views.mechanic_views import MechanicList
from tp2_app.views.appointment_views import AppointmentList
from tp2_app.views.vehicle_views import VehicleList


def statistics(request):
    client_data = {
        'count': Client.objects.count(),
        'status': __get_status_code(ClientList),
    }

    mecano_data = {
        'count': Mechanic.objects.count(),
        'status': __get_status_code(MechanicList),
    }

    appointment_data = {
        'count': Appointment.objects.count(),
        'status': __get_status_code(AppointmentList),
        'accepted_appointment_count' : Appointment.objects.filter(is_accepted=True).count(),
        'refused_appointment_count' : Appointment.objects.filter(is_accepted=False).count()
    }

    vehicle_data = {
        'count': Vehicle.objects.count(),
        'status': __get_status_code(VehicleList),
    }

    bill_data = {
        'count' : Bill.objects.count(),
        'status': __get_status_code(BillList),
        'paid_bill_count': Bill.objects.filter(is_paid=True).count(),
        'unpaid_bill_count': Bill.objects.filter(is_paid=False).count(),
    }

    user_count = client_data.get('count') + mecano_data.get('count')

    context = {
        'client_data': client_data,
        'mecano_data' : mecano_data,
        'appointment_data' : appointment_data,
        'vehicle_data' : vehicle_data,
        'bill_data' : bill_data,
        'user_count' : user_count,
        'username': 'xX_Gooner69_Xx',
    }
    return render(request, 'statistic.html', context)


def __get_status_code(view_class):
    factory = APIRequestFactory()
    request = factory.get(f'/{view_class.__name__.lower()}/')
    view = view_class.as_view()
    response = view(request)
    return response.status_code
