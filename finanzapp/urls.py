from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # 👈

urlpatterns = [
    path('', lambda request: redirect('transacciones/')),  # 👈 redirección por defecto
    path('admin/', admin.site.urls),
    path('transacciones/', include('transacciones.urls')),
]
