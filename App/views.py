from operator import index
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required

# Importaciones para la autenticación y registro
from django.contrib.auth import login, authenticate
from .forms import *  # Asegúrate de que estás importando tu formulario SignUpForm
from .models import *
from django.db.models import Q
from django.contrib import messages
# Create your views here.
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
        ).order_by('-id_producto')[-1]
    data={
        'forms':buscar
    }
    return render(request,'Pages/visualizar.html',data)

def verMas(request,id_producto):
    buscar=Productos.objects.filter(id_producto=id_producto)
    data={
        'forms':buscar
    }
    return render(request,'Pages/vermas.html',data)

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
    return redirect(to="visualizar")


def salir(request):
    logout(request)
    return redirect(to='inicio')

@login_required
def Comprar (request,id_producto):
    try:
        usuario = User.objects.get_by_natural_key(request.user.username)

        carrito = Carrito.objects.all().get_or_create(carrito_id=request.user.id,user=usuario)
        carritoDet = Carrito_detalle.objects.create(carrito_det=Carrito.objects.last(),producto=get_object_or_404(Productos,id_producto=id_producto),cantidad=1)
        carritoDet.save()
        return redirect("inicio")
    except Carrito.DoesNotExist:
            try:
                NCarr = Carrito(user=usuario)
                NCarr.save()
            except NCarr.DoesNotExist:
                return redirect("inicio")
def VerCarrito (request):
    #sql = Carrito_detalle.objects.select_related('carrito_det','producto').all().filter(carrito_det__user=request.user.username)
    try:
        sql = Carrito_detalle.objects.filter(carrito_det__user=request.user.id)

        data = {
            'forms':sql
        }
        return render(request,"Pages/carrito.html",data)
    except Carrito_detalle.DoesNotExist:
        return render (request,"index.html",{"data":"Carrito no encontrado"})
def EliminarCarrito (request):
    try:
        sql = Carrito_detalle.objects.filter(carrito_det__user=request.user.id)

        data = {
            'forms':sql
        }
        return render(request,"Pages/carrito.html",data)
    except Carrito_detalle.DoesNotExist:
        return render (request,"index.html",{"data":"Carrito no encontrado"})
    
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
