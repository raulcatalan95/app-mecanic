from django.db import models

class Representantes(models.Model):
    rutRepresentante=models.CharField(primary_key=True,max_length=15)
    nombre = models.CharField(max_length=100,blank=False)
    correo = models.CharField(max_length=75,blank=False)
    clave = models.CharField(max_length=50,blank=False)
    telefono = models.CharField(max_length=15,blank=False)
    fechaNacimiento = models.DateField(null=False,blank=False)

   
class Talleres(models.Model):
    rutTaller = models.CharField(primary_key=True,max_length=20)
    razonSocial = models.CharField(max_length=100,blank=False)
    comuna = models.CharField(max_length=30,blank=False)
    direccion = models.CharField(max_length=100,blank=False)
    telefono = models.CharField(max_length=15,blank=False)
    correo = models.CharField(max_length=75,blank=False)
    pagina = models.CharField(max_length=50,null=True,blank=True)
    rutRepresentante = models.ForeignKey(Representantes,null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.rutTaller

    def get_absolute_url(self):
        return "/vista_talleres/%i" %self.id

class Clientes(models.Model):
    rutCliente = models.CharField(primary_key=True,max_length=15,blank=False)
    correo = models.CharField(max_length=75,blank=False)
    fechaNacimiento = models.DateField(null=False)
    nick = models.CharField(max_length=75,blank=False)
    clave = models.CharField(max_length=75,null=False)
    tipoVehiculo = models.CharField(max_length=75,blank=False)
    patente = models.CharField(max_length=75,blank=False)
    modelo = models.CharField(max_length=75)
    marca = models.CharField(max_length=75)
    anno = models.ImageField()

    def __str__(self):
        return self.rutCliente

    def get_absolute_url(self):
        return "/vista_clientes/%i" %self.id

class Comentarios(models.Model):
    comentario = models.CharField(max_length=200,null=False)
    evaluacion = models.IntegerField(null=False)
    rutTaller = models.ForeignKey(Talleres,null=True,blank=True,on_delete=models.CASCADE)
    rutCliente = models.ForeignKey(Clientes,null=True,blank=True,on_delete=models.CASCADE)
    fecha = models.DateField(null=False)

class CategoriasDisponibles(models.Model):
    idCategoria = models.CharField(primary_key=True,max_length=5)
    nombreCategoria = models.CharField(max_length=25,blank=False)

class listadoCategorias(models.Model):
    idCategoria = models.ForeignKey(Representantes,on_delete=models.CASCADE)
    rutTaller = models.ForeignKey(Talleres,on_delete=models.CASCADE)

class ServiciosDisponibles(models.Model):
    idServicios = models.CharField(primary_key=True,max_length=5)
    nombreServicio = models.CharField(max_length=25, null=False)

class listadoPrecios(models.Model):
    precio = models.CharField(max_length=25, null=False)
    rutTaller = models.ForeignKey(Talleres,on_delete=models.CASCADE)
    idServicios = models.ForeignKey(ServiciosDisponibles,null=True,blank=True,on_delete=models.CASCADE)

class Clasificacion(models.Model):
    taller = models.ForeignKey(Talleres,null=True,blank=True,on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False,default=0)
    promedio = models.FloatField(null=False,default=0)

class FechaRegistro(models.Model):
    rut = models.CharField(primary_key=True,max_length=30)
    fecha = models.DateField(null=False)
    tipo = models.CharField(max_length=100,null=False,default="-")
    # acion = models.CharField(max_length=100,null=False,default="-")