from django.contrib import admin
from django.urls import path, include
from catalog.ml_auth import ml_autorizar

urlpatterns = [
    path('admin/ml-autorizar/', ml_autorizar),
    path('admin/', admin.site.urls),
    path('api/', include('catalog.urls')),
]
