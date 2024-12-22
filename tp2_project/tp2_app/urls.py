from django.http import HttpResponseRedirect
from django.urls import path, re_path, reverse
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views.home_views import home, lobby
from .views.login_views import login
from .views.register_views import register
from .views.statistic_views import statistics
from .views.client_views import ClientList, ClientCreate, ClientDetail
from .views.mechanic_views import MechanicList, MechanicCreate, MechanicDetail
from .views.vehicle_views import VehicleList, VehicleCreate, VehicleDetail
from .views.bill_views import BillList, BillCreate, BillDetail
from .views.appointment_views import AppointmentList, AppointmentCreate, AppointmentDetail

schema_view = get_schema_view(
    openapi.Info(
        title="Titre",
        default_version="v1.0",
        description="Description"
    ),
    public=True,
)

urlpatterns = [
    path('', lobby, name="home"),
    path('lobby/', lobby, name="lobby"),

    path('login/',login, name="login"),
    path('register/', register, name='register'),

    path('statistics/',statistics, name="statistics"),

    # Swagger path
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),

    # Client paths
    path('clients/', ClientList.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetail.as_view(), name='client-detail'),
    path('clients/create/', ClientCreate.as_view(), name='client-create'),

    # Mechanic paths
    path('mechanics/', MechanicList.as_view(), name='mechanic-list'),
    path('mechanics/<int:pk>/', MechanicDetail.as_view(), name='mechanic-detail'),
    path('mechanics/create/', MechanicCreate.as_view(), name='mechanic-create'),

    # Vehicle paths
    path('vehicles/', VehicleList.as_view(), name='vehicle-list'),
    path('vehicles/<int:pk>/', VehicleDetail.as_view(), name='vehicle-detail'),
    path('vehicles/create/', VehicleCreate.as_view(), name='vehicle-create'),

    # Bill paths
    path('bills/', BillList.as_view(), name='bill-list'),
    path('bills/<int:pk>/', BillDetail.as_view(), name='bill-detail'),
    path('bills/create/', BillCreate.as_view(), name='bill-create'),

    # Appointment paths
    path('appointments/', AppointmentList.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', AppointmentDetail.as_view(), name='appointment-detail'),
    path('appointments/create/', AppointmentCreate.as_view(), name='appointment-create'),
    re_path(r'^.*$', lambda request: HttpResponseRedirect(reverse('lobby'))),
]
