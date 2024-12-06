from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views #necesario para la contraseña
from .mercadopago import create_preference
urlpatterns = [
    #pantallas
    path( '',Home,name='inicio'),
    path('contacto/',Contacto,name='contacto'),
    path('nosotros/',Nosotros,name='nosotros'),
    #carrito
    path('carrito/<id_producto>/',AgregarCarrito,name='compcarrito'),
    path('carrito/',VerCarrito ,name='carrito'),
    path('carrito/eliminar/<pk_carritodet>/',EliminarCarrito ,name='carritoE'),
    path('carrito/modificar/<int:pk_carritodet>/', ModificarCantidad, name='modificar_cantidad'),
    path('comprar/<int:id_producto>/<int:pk_carritodet>',comprar_producto ,name='comprar'),
    path('pagar/<pk_carritodet>/',payment,name='payment'),
    path('pagar/',payment,name='paymentfull'),
    path('comprar_todo_carrito/',comprar_todo_carrito,name='comprar_todo_carrito'),
    #productos
    path('productos/',ver_Productos,name='visualizar'),
    path('agregar/',Agregar,name='agregar'),
    path('modificar/<id_producto>/',Modificar_Productos,name='modificar'),
    path('eliminar/<id_producto>/',Eliminar_Productos,name='eliminar'),
    path('producto/<id_producto>/',verMas,name='vermas'),
    #usuario
    path('logouts/',salir,name='logouts'),
    path('register/', register, name='register'),
    path('mails/',Gmail,name='gmail'),
    path('profile/',user_profile,name='profile'),
    #reseteo de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #mercadopago
    path("create_preference/",create_preference, name="preference")
]
