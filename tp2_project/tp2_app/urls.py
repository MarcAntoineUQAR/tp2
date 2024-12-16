from django.urls import path, include
from .views import home
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('', home, name="home"),
]