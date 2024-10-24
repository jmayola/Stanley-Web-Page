from django.urls import path
#-->Importamos las Vistas para las URL
from .views import *

urlpatterns = [
    #-->URL, FUNCION, NOMBRE PARA HTML
    path( '',Home,name='inicio'),
    path('agregar/',Agregar,name='agregar'),
    path('comprar/<id_producto>/',Comprar,name='comprar'),
    path('carrito/',VerCarrito ,name='carrito'),
    path('carrito/eliminar/<pk_carritodet>/',EliminarCarrito ,name='carritoE'),
    path('productos/',ver_Productos,name='visualizar'),
    path('modificar/<id_producto>/',Modificar_Productos,name='modificar'),
    path('eliminar/<id_producto>/',Eliminar_Productos,name='eliminar'),
    path('logouts/',salir,name='logouts'),
    path('register/', register, name='register'),
    path('producto/<id_producto>/',verMas,name='vermas')
]
