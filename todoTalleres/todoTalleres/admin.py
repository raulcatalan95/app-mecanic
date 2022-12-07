from . import models
from django.contrib import admin

admin.site.register(models.Representantes)
admin.site.register(models.Talleres)
admin.site.register(models.Clientes)
admin.site.register(models.Comentarios)
admin.site.register(models.CategoriasDisponibles)
admin.site.register(models.ServiciosDisponibles)
admin.site.register(models.listadoPrecios)
admin.register(models.Clientes, models.Representantes)
