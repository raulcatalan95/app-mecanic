from django.shortcuts import render, redirect
from . import models

def renderBase(request):
    return render(request,'base.html')

#Registro de cliente
def agregarClientes(request):
    try:
        mensaje = ""
        rutCliente = request.POST['rutCliente']
        correo = request.POST['correo']
        fechaNacimiento = request.POST['fechaNacimiento']
        nick = request.POST['nick']
        clave = request.POST['clave']
        tipoVehiculo = request.POST['tipoVehiculo']
        patente = request.POST['patente']
        modelo = request.POST['modelo']
        marca = request.POST['marca'] 
        anno = request.POST['anno']

        models.Clientes.objects.create(rutCliente = rutCliente,correo=correo, fechaNacimiento=fechaNacimiento, nick=nick, clave=clave, tipoVehiculo=tipoVehiculo, patente=patente,
        modelo=modelo,marca=marca,anno=anno)

        mensaje = f"Se ha regitrado el Cliente {rutCliente}"
    except Exception as ex:
        if str(ex.__cause__).find('todoTalleres_clientes.rutCliente') > 0:
            mensaje = 'Ya existe un registro con ese rut'
    except Error as err:
            mensaje = f'ha ocurrido un problema en la operación_, {err}'
    except:
        return render(request,"CRUD_clientes/agregarClientes.html",{'mensaje':mensaje})  
    return render(request,"CRUD_clientes/agregarClientes.html",{'mensaje':mensaje})  


#Registro de taller
def agregarTaller(request):
    try:
        mensaje = ""
        rutTaller = request.POST['rutCliente']
        razonSocial = request.POST['correo']
        comuna = request.POST['fechaNacimiento']
        direccion = request.POST['nick']
        telefono = request.POST['clave']
        correo = request.POST['tipoVehiculo']
        pagina = request.POST['patente']
        rutRepresentante = request.POST['modelo']

        models.Talleres.objects.create(rutTaller = rutTaller,razonSocial=razonSocial, comuna=comuna, direccion=direccion, telefono=telefono, correo=correo, pagina=pagina,
        rutRepresentante=rutRepresentante)

        mensaje = f"Se ha regitrado el Cliente {rutTaller}"
    except Exception as ex:
        if str(ex.__cause__).find('todoTalleres_talleres.rutTaller') > 0:
            mensaje = 'Ya existe un registro con ese rut'
    except Error as err:
            mensaje = f'ha ocurrido un problema en la operación_, {err}'
    except:
        return render(request,"CRUD_talleres/agregarTaller.html",{'mensaje':mensaje})  
    return render(request,"CRUD_talleres/agregarTaller.html",{'mensaje':mensaje})  
    

   

