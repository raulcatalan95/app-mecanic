from django.shortcuts import render, redirect
from . import models
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib.auth import logout
from msilib.schema import Error
from datetime import date

clientes = []
representantes = []

def vistaClientes(request):
    sesion = None
    context = None
    try:
        sesion = request.session['sesion_activa']
        if sesion != 0 and sesion !=1:
            sesion = None
    except:
        sesion = None
    return render(request, "vista_clientes.html", {'sesion_activa': sesion})
 
def vistaTalleres(request):
    return render(request,'vista_talleres.html')

def renderBase(request):
    return render(request,'index.html')
    
#inicio de sesion
def irInicioSesion(request):
    try:
        if request.session['sesion_activa'] == 0:
            del request.session['sesion_activa']
            clientes.clear()
            return render(request,"vista_clientes.html")
        elif request.session['sesion_activa'] == 1:
            del request.session['sesion_activa']
            representantes.clear()
            return render(request,"vista_talleres.html")
        else:
            return render(request,"sesion/login.html")   
    except:
        return render(request,"sesion/login.html")
        
def fxInicioSesion(request):
    usr = None
    try:
        usr = models.Clientes.objects.get(nick = request.POST["form_username"])
        if (usr.clave == request.POST["form_password"]):
            request.session['sesion_activa'] = 0
            sesion = request.session['sesion_activa']
            clientes.append(usr.nick)
            clientes.append(usr.clave)
            return render(request,"vista_clientes.html",{"cliente":usr,"sesion_activa":sesion})
        else:
             return render(request,"sesion/login.html"), {"mensaje":"contraseña no válida"}  
    except:
        usr = None
        try:
            usr = models.Representantes.objects.get(correo = request.POST["form_username"])
            if (usr.clave == request.POST["form_password"]):
                request.session['sesion_activa'] = 1
                sesion = request.session['sesion_activa']
                representantes.append(usr.correo)
                representantes.append(usr.clave)
                return render(request,"vista_talleres.html",{"taller":usr,"sesion_activa":sesion})
            else:
                return render(request,"sesion/login.html"), {"mensaje":"contraseña no válida"}  
        except:
            try:
                usr = models.Clientes.objects.get(nick = clientes[0])
                if(usr.clave == clientes[1]):
                    request.session['sesion_activa'] = 0
                    sesion = request.session['sesion_activa']   
                return render(request,"vista_clientes.html",{"cliente":usr,"sesion_activa":sesion})
            except:
                usr = None
                try:
                    usr = models.Representantes.objects.get(correo = representantes[0])
                    if (usr.clave == representantes[1]):
                     request.session['sesion_activa'] = 1
                     sesion = request.session['sesion_activa']
                     return render(request,"vista_talleres.html",{"taller":usr,"sesion_activa":sesion})
                    else:
                     return render(request,"sesion/login.html"), {"mensaje":"contraseña no válida"}  
                except:
                    return render(request,"sesion/login.html")
               
           

#editar cliente
def editar_cliente(request,rutCliente):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return redirect("sesion/login.html")

    if sesion == 0:
        atencion = models.Clientes.objects.get(rutCliente=rutCliente)
        form = forms.clienteForm(request.POST or None, request.FILES or None, instance=atencion)
        if form.is_valid() and request.POST:
            form.save()
            return redirect(fxInicioSesion)
        return render(request,'CRUD_clientes/editar_cliente.html',{'form': form,'sesion_activa':sesion})
    else:
        return redirect(irInicioSesion)
#editar taller
def editar_taller(request,rutRepresentante):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "sesion/login.html")
    if sesion==1:
        atencion = models.Talleres.objects.get(rutRepresentante=rutRepresentante)
        form = forms.tallerForm(request.POST or None, request.FILES or None, instance=atencion)
        if form.is_valid() and request.POST:
           form.save()
           return redirect(fxInicioSesion)
        return render(request,'CRUD_talleres/editar_taller.html',{'form': form,'sesion':sesion})
    else:
        return redirect(irInicioSesion)


#Registro de cliente
def registro_cliente(request):
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
        models.FechaRegistro.objects.create(rut = rutCliente,fecha = date.today(),tipo = "Cliente" )

        mensaje = f"Se ha regitrado el Cliente {rutCliente}"
    except Exception as ex:
        if str(ex.__cause__).find('todoTalleres_clientes.rutCliente') > 0:
            mensaje = 'Ya existe un registro con ese rut'
    except Error as err:
            mensaje = f'ha ocurrido un problema en la operación_, {err}'
    except:
        return render(request,"CRUD_clientes/registro_cliente.html",{'mensaje':mensaje})  
    return render(request,"CRUD_clientes/registro_cliente.html",{'mensaje':mensaje})  


#Registro de taller
def registro_taller(request):
    try:
        mensaje = ""
        rutTaller = request.POST['rutTaller']
        razonSocial = request.POST['razonSocial']
        comuna = request.POST['comuna']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        pagina = request.POST['pagina']
        rutRepresentante = request.POST['rutRepresentante']
        rutModel=  models.Representantes.objects.get(rutRepresentante = rutRepresentante)

        models.Talleres.objects.create(rutTaller = rutTaller,razonSocial=razonSocial, comuna=comuna, direccion=direccion, telefono=telefono, correo=correo, pagina=pagina,
        rutRepresentante=rutModel)
        models.FechaRegistro.objects.create(rut = rutTaller,fecha = date.today(),tipo = "Taller" )

        mensaje = f"Taller creado: {rutModel}"
        return render(request,"CRUD_talleres/registro_taller.html",{'mensaje':mensaje})  

    except Exception as ex:
        if str(ex.__cause__).find('todoTalleres_talleres.rutTaller') > 0:
            mensaje = 'Ya existe un registro con ese rut'
    except Error as err:
            mensaje = f'ha ocurrido un problema en la operación_, {err}'
    except:
          return render(request,"CRUD_talleres/registro_taller.html",{'mensaje':mensaje})  
    return render(request,"CRUD_talleres/registro_taller.html",{'mensaje':mensaje})    

       
#agregar Representante
def registro_representante(request):
    try:
        mensaje = ""
        rutRepresentante = request.POST['rutRepresentante']
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        clave = request.POST['clave']
        telefono = request.POST['telefono']
        fechaNacimiento = request.POST['fechaNacimiento']
        models.Representantes.objects.create(rutRepresentante = rutRepresentante,nombre=nombre, correo=correo, clave=clave, telefono=telefono, fechaNacimiento=fechaNacimiento)
        models.FechaRegistro.objects.create(rut = rutRepresentante,fecha = date.today(),tipo = "Representante" )

        mensaje = f"Se ha regitrado el Cliente {rutRepresentante}"
    except Exception as ex:
        if str(ex.__cause__).find('todoTalleres_representantes.rutRepresentante') > 0:
            mensaje = 'Ya existe un registro con ese rut'
    except Error as err:
            mensaje = f'ha ocurrido un problema en la operación_, {err}'
    except:
        return render(request,"CRUD_talleres/registro_representante.html",{'mensaje':mensaje})  
    return render(request,"CRUD_talleres/registro_representante.html",{'mensaje':mensaje})  


#Buscar talleres

def buscar_talleres(request):
    sesion = None
    try:
        sesion = request.session["sesion_activa"]
    except:
        mensaje=""
        return render(request, "sesion/login.html", {'sesion_activa': sesion,'mensaje':mensaje})

    mensaje = None
    visibilidad = "visible"
    talleres = ""
    try:
        buscador = request.GET["buscar"]
        talleres = models.Talleres.objects.filter()

        if buscador:
           talleres = models.Talleres.objects.filter(
               Q(rutTaller__contains = buscador) |
               Q(telefono__contains = buscador) |
               Q(razonSocial__contains = buscador) |
               Q(comuna__contains = buscador) |
               Q(direccion__contains = buscador) |
               Q(correo__contains = buscador) |
               Q(pagina__contains = buscador)).distinct()

        visibilidad = "visible"
        return render(request, 'CRUD_talleres/buscar_talleres.html',{'mensaje':mensaje,"talleres":talleres,"visibilidad":visibilidad,'sesion_activa': sesion})
    except:
                   mensaje = ''
                   return render(request, 'CRUD_talleres/buscar_talleres.html',{'mensaje':mensaje,"visibilidad":visibilidad,'sesion_activa': sesion})

#Eliminar Cliente
def eliminar_cliente(request):
    mensaje = None
    try:
        usr = models.Clientes.objects.get(rutCliente = request.GET["rutClienteFormulario"])
        if usr:
             usr.delete()
             mensaje = "Cuenta eliminada"
             return render(request, 'base.html',{'mensaje':mensaje})

        mensaje="Ingrese su rut correctamente "
        return render(request, 'CRUD_clientes/eliminar_cliente.html',{'mensaje':mensaje})
    except Exception as ex:
        if str(ex.args).find('does not exist') > 0:
            mensaje = 'Rut no coincide'
        else:
            mensaje = 'Ha ocurrido un problema'        
        return render(request, 'CRUD_clientes/eliminar_cliente.html',{'mensaje':mensaje})

# FUNCIONES DE PRUEBA // ELIMINAR

def irAgregarComentario(request):
    return render(request,'test/agregarComentario.html')

def fxAgregarComentario(request):
    msj = None

    #_id = request.GET['id'] 
    _comentario = request.GET['comentario']
    _evaluacion = request.GET['evaluacion']
    _rutTaller = request.GET['rutTaller']
    _rutCliente = request.GET['rutCliente']
    
    try:
        models.Comentarios.objects.create(
            #id = _id, 
            comentario = _comentario, 
            evaluacion = _evaluacion, rutTaller = _rutTaller,
            rutCliente = _rutCliente, fecha = date.today())
        msj = 'comentario registrado'
    except Error as err:
        msj = f'\n Ha ocurrido un error en la operacion {err}'
    return render(request,'test/agregarComentario.html', {'msj': msj}) 
