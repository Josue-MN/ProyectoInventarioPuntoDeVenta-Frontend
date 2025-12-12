"""
URL configuration for ProyectoInventarioPuntoDeVenta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from LoginApp.views import renderlogin as Login
from AdminHomeApp import views as AdminHomeApp
from CrudBodegasApp import views

# Lista de rutas principales de la aplicación Django
urlpatterns = [
    # Ruta para el panel de administración de Django
    # Cuando accedes a /admin/ se abre el admin predeterminado de Django
    path('admin/', admin.site.urls),

    # Ruta principal del login
    # Todas las URLs definidas en LoginApp.urls se incluirán aquí
    # Al acceder a la raíz del sitio ("/") se manejarán las vistas de LoginApp
    path('', include('LoginApp.urls')),

    # Ruta para el home del administrador
    # Todas las URLs definidas en AdminHomeApp.urls se incluirán bajo /adminhome/
    path('adminhome/', include('AdminHomeApp.urls')),

    # Ruta para el home general de la aplicación
    # Todas las URLs definidas en HomeApp.urls se incluirán bajo /home/
    path('home/', include("HomeApp.urls")),

    path('bodegas/', include('CrudBodegasApp.urls')),
]

