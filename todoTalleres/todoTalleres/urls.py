"""todoTalleres URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.renderBase),
    path('login',views.irInicioSesion),
    path('fxInicioSesion', views.fxInicioSesion),
    path('registro_cliente',views.registro_cliente),
    path('registro_taller',views.registro_taller),
    path('registro_representante',views.registro_representante),
    path('buscar_talleres',views.buscar_talleres),
    path('eliminar_cliente',views.eliminar_cliente),
    path('actualizar_taller',views.actualizar_taller),
    path('editar_cliente/<str:rutCliente>',views.editar_cliente,name='editar_cliente'),
    path('editar_taller/<str:rutRepresentante>',views.editar_taller,name='editar_taller'),
]
