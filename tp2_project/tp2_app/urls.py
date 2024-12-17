from django.urls import path
from .views import home, ClientDetail, ClientCreate
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Titre",
        default_version="v1.0",
        description="Description"
    ),
    public=True,
)

urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path('', home, name="home"),
    path('clients/', ClientCreate.as_view(), name='client-create'),
    path('clients/<int:pk>/', ClientDetail.as_view(), name='client-detail'),
]
