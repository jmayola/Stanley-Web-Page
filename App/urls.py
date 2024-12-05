from django.urls import path
#-->Importamos las Vistas para las URL
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    #-->URL, FUNCION, NOMBRE PARA HTML
    path( '',Home,name='inicio'),
    path('agregar/',Agregar,name='agregar'),
    path('carrito/<id_producto>/',AgregarCarrito,name='compcarrito'),
    path('carrito/',VerCarrito ,name='carrito'),
    path('carrito/eliminar/<pk_carritodet>/',EliminarCarrito ,name='carritoE'),
    path('comprar/<int:id_producto>/<int:cantidad>',comprar_producto ,name='comprar'),
    path('productos/',ver_Productos,name='visualizar'),
    path('modificar/<id_producto>/',Modificar_Productos,name='modificar'),
    path('eliminar/<id_producto>/',Eliminar_Productos,name='eliminar'),
    path('logouts/',salir,name='logouts'),
    path('register/', register, name='register'),
    path('producto/<id_producto>/',verMas,name='vermas'),
    path('mails/',Gmail,name='gmail'),
    path('comprar_todo_carrito/',comprar_todo_carrito,name='comprar_todo_carrito'),
    path('contacto/',Contacto,name='contacto'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
