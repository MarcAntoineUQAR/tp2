from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/tp2_app/login/', permanent=False)),

    path('admin/', admin.site.urls),
    path('tp2_app/', include('tp2_app.urls')),
]
