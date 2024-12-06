from operator import index
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
# Importaciones para la autenticación y registro
from django.contrib.auth import login, authenticate
from .forms import *  # Asegúrate de que estás importando tu formulario SignUpForm
from .models import *
from django.db.models import Q
from django.contrib import messages
# Create your views here.

#email
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
def Home(request):
    buscar=Productos.objects.all().order_by('-id_producto')[:3]
    data={
        'forms':buscar
    }
    return render (request,'index.html',data)

def ver_Productos(request):
    #--->TREAMOS TODOS LOS ELEMENTOS DEL TABLA
    buscar=Productos.objects.all()
    filtro=request.GET.get("filtro")
    if filtro:
        buscar = Productos.objects.filter(
            Q(nom_producto__icontains=filtro)
        ).order_by('-id_producto')
    data={
        'forms':buscar
    }
    return render(request,'Pages/visualizar.html',data)

def verMas(request, id_producto):
    buscar = get_object_or_404(Productos, id_producto=id_producto)
    data = {
        'producto': buscar  
    }
    return render(request, 'Pages/vermas.html', data)
@login_required

@permission_required('App.add_personajes')
def Agregar(request):
    data={
        'forms':NuevoProducto()
    }
    if request.method=='POST':
        query=NuevoProducto(data=request.POST,files=request.FILES)
        if  query.is_valid():
            query.save()
            data['mensaje']="Datos Registrados"
            messages.success(request,"Producto Registrado")
        else:
            data['forms']=NuevoProducto
    return render (request,'Pages/agregar.html',data)


@permission_required('App.change_personajes')
def Modificar_Productos(request,id_producto):
    sql=get_object_or_404(Productos,id_producto=id_producto)
    data={
        'forms':NuevoProducto(instance=sql)
    }
    if request.method=='POST':
        query=NuevoProducto(data=request.POST,instance=sql,files=request.FILES)
        if  query.is_valid():
            query.save()
            data['mensaje']="Datos Modificados Correctamente "
        else:
            data['forms']=NuevoProducto
    return render (request,'Pages/modificar.html',data)


@permission_required('App.delete_personajes')
def Eliminar_Productos(request,id_producto):
    buscar=get_object_or_404(Productos,id_producto=id_producto)
    buscar.delete()
    return redirect(to="carrito")

@login_required
def salir(request):
    logout(request)
    return redirect(to='inicio')

@login_required
def AgregarCarrito (request,id_producto):
    try:
        usuario = User.objects.get_by_natural_key(request.user.username)
        carrito = Carrito.objects.get(user=usuario)
        Carrito_detalle.objects.create(carrito_det=carrito,producto=get_object_or_404(Productos,id_producto=id_producto),cantidad=request.POST["quantity"])
        return redirect("inicio")
    except Carrito.DoesNotExist:
            try:
                NCarr = Carrito(user=usuario)
                NCarr.save()
                return redirect("inicio")
            except NCarr.DoesNotExist as e:
                print(e)
                return redirect("inicio")
            
@login_required
def VerCarrito (request):
    sql = Carrito_detalle.objects.select_related('carrito_det','producto').all().filter(carrito_det__user=request.user.id)
    try:
        sql = Carrito_detalle.objects.filter(carrito_det__user=request.user.id)

        data = {
            'forms':sql
        }
        return render(request,"Pages/carrito.html",data)
    except Carrito_detalle.DoesNotExist:
        return render (request,"index.html",{"data":"Carrito no encontrado"})
    
@login_required
def EliminarCarrito (request,pk_carritodet):
    buscar=get_object_or_404(Carrito_detalle,pk_carritodet=pk_carritodet)
    buscar.delete()
    return redirect(to="carrito")

@login_required
def ModificarCantidad(request, pk_carritodet):
    if request.method == 'POST':
        nueva_cantidad = int(request.POST['quantity'])
        carrito_detalle = get_object_or_404(Carrito_detalle, pk_carritodet=pk_carritodet)

        # Validar que la nueva cantidad no exceda el stock
        if nueva_cantidad <= carrito_detalle.producto.stock_producto:
            carrito_detalle.cantidad = nueva_cantidad
            carrito_detalle.save()
            return redirect('carrito')
        else:
            # manejar el caso donde la cantidad excede el stock
            messages.error(request, f"Lo siento, no hay stock disponible para {carrito_detalle.producto.nom_producto}.")
            return render(request, 'Pages/sin_stock.html', {'producto': carrito_detalle.producto})
@login_required
def payment(request, pk_carritodet=None):
    if pk_carritodet:  # si se proporciona pk_carritodet, se compra un solo producto
        carrito_detalle = get_object_or_404(Carrito_detalle, pk_carritodet=pk_carritodet)
        cantidad = carrito_detalle.cantidad
        if cantidad <= carrito_detalle.producto.stock_producto:
            total = carrito_detalle.cantidad * carrito_detalle.producto.precio_producto
            return render(request, "Pages/payment.html", {"product": carrito_detalle, "total": total})
        else:
            messages.error(request, f"Lo siento, no hay stock disponible para {carrito_detalle.producto.nom_producto}.")
            return render(request, 'Pages/sin_stock.html', {'producto': carrito_detalle.producto})
    else:  #si no se proporciona pk_carritodet, se compran todos los productos del carrito
        usuario = request.user
        carrito = get_object_or_404(Carrito, user=usuario)
        detalles = Carrito_detalle.objects.filter(carrito_det=carrito)

        #verificar el stock de cada producto
        for detalle in detalles:
            if detalle.cantidad > detalle.producto.stock_producto:
                messages.error(request, f"Lo siento, no hay stock disponible para {detalle.producto.nom_producto}.")
                return render(request, 'Pages/sin_stock.html', {'producto': detalle.producto})

        # Si todo está en orden, renderiza la página de pago
        return render(request, "Pages/payment.html", {"products": detalles})
@login_required
def comprar_todo_carrito(request):
    # Obtener el carrito del usuario autenticado
    carrito = get_object_or_404(Carrito, user=request.user)
    
    # Obtener todos los detalles del carrito
    detalles_carrito = Carrito_detalle.objects.filter(carrito_det=carrito)

    # Lista para almacenar los resultados de las compras
    resultados_compra = []

    for detalle in detalles_carrito:
        producto = detalle.producto
        
        # Verificar si hay suficiente stock para cada producto
        if producto.stock_producto >= detalle.cantidad:
            # Actualizar el stock del producto
            producto.stock_producto -= detalle.cantidad
            
            # Crear la compra
            try:
                print((producto.nom_producto,detalle.cantidad,producto.precio_producto))
                compra = Compra.objects.create(
                   usuario=request.user,
                   producto=producto,
                   cantidad=detalle.cantidad,
                   precio_total=producto.precio_producto * detalle.cantidad
                )
                producto.save()
                compra.save()  # Guardar el cambio en el stock
                resultados_compra.append(f"Has comprado {detalle.cantidad} de {producto.nom_producto} con éxito.")
            except Exception as e:
                print(e)
                resultados_compra.append(f"No se ha podido comprar {producto.nom_producto}.")
        else:
            resultados_compra.append(f"Lo siento, no hay suficiente stock para {producto.nom_producto}.")

    # Limpiar el carrito después de la compra
    detalles_carrito.delete()

    # Mensaje final sobre la compra
    if resultados_compra:
        messages.success(request, "Resultados de tu compra: " + " | ".join(resultados_compra))
    else:
        messages.error(request, "No se realizaron compras.")

    return redirect('visualizar')  # Redirigir a la página de visualización de productos o donde desees
# Nueva vista para el registro de usuarios
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Cambiar a SignUpForm
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(to='inicio')  # Redirigir al home después de registrarse
    else:
        form = SignUpForm()  # Crear un nuevo formulario vacío
    return render(request, 'registration/register.html', {'form': form})
def Gmail(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        email = request.POST["email"]
        asunto = request.POST["asunto"]
        mensaje = request.POST["mensaje"]

        # Renderizar la plantilla con el contexto adecuado
        plantilla = render_to_string("Pages/email.html", {
            'nombre': nombre,
            'email': email,
            'asunto': asunto,
            'mensaje': mensaje,
        }, request=request)

        contenido = EmailMessage(
            asunto, plantilla, settings.EMAIL_HOST_USER, ['julianmayola131@gmail.com']
        )
        contenido.content_subtype = "html"
        contenido.send(fail_silently=True)

        messages.success(request, 'Datos enviados correctamente.')
        return redirect(to="inicio")

    # Si no es un POST, renderiza el formulario o redirige
    return render(request, 'Pages/contacto.html')  # Asegúrate de tener una plantilla para el formulario
def Contacto (request):
    return render(request,"Pages/contacto.html")
def Nosotros (request):
    return render(request,"Pages/nosotros.html")

@login_required
def user_profile(request):
    return render(request, 'Pages/user_profile.html', {'user': request.user})

def comprar_producto(request, id_producto,pk_carritodet):
    producto = get_object_or_404(Productos, id_producto=id_producto)  # Busca el producto por código
    cantidad = request.POST["quantity"]
    # Simulamos la compra verificando el stock disponible
    if producto.stock_producto > 0:
        producto.stock_producto -= int(cantidad)

        # Crear la compra
        try:
            compra = Compra.objects.create(
                usuario=request.user,  # Usuario autenticado
                producto=producto,    
                cantidad=cantidad,          
                precio_total=int(producto.precio_producto) * int(cantidad) # El precio total es igual al precio del producto
            )
            producto.save()  
            compra.save()  # Guardar la compra en la base de datos
            detalles_carrito = get_object_or_404(Carrito_detalle, pk_carritodet=pk_carritodet)
            detalles_carrito.delete()
            plantilla = render_to_string("Pages/confirmacion_compra.html", {
            'producto': producto,
            'compra': compra,
            }, request=request)

            contenido = EmailMessage(
                "Compra Confirmada - Stanley", plantilla, settings.EMAIL_HOST_USER, [request.user.email]
            )
            contenido.content_subtype = "html"
            contenido.send(fail_silently=True)
            messages.success(request, f"Has comprado {producto.nom_producto} con éxito.")
            return render(request, 'Pages/confirmacion_compra.html', {'producto': producto, 'compra':compra})
        except Exception as e:
            print(e)
            messages.error(request, f"No se ha podido comprar {producto.nom_producto}.")
            return redirect('login')

    else:
        messages.error(request, f"Lo siento, no hay stock disponible para {producto.nom_producto}.")
        return render(request, 'Pages/sin_stock.html', {'producto': producto})