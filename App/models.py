from django.db import models
from ckeditor import fields
from django.contrib.auth.models import User
# Create your models here.
class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nom_producto = models.TextField(max_length=50, null=False)
    desc_producto = fields.RichTextField(null=True)
    precio_producto = models.IntegerField(null=False)
    stock_producto = models.IntegerField(null=False)
    imagen_producto = models.ImageField(null=False,upload_to="productos", default="")
    def __int__ (self):
        return self.id_producto

class Carrito(models.Model):
    carrito_id = models.AutoField(primary_key=True, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __int__(self):
        return self.carrito_id
    
class Carrito_detalle(models.Model):
    pk_carritodet = models.AutoField(primary_key=True, null=False)
    carrito_det = models.ForeignKey(Carrito, on_delete=models.CASCADE, null=False)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"Carrito de {self.carrito_det.user} con el producto {self.producto.nom_producto}"
class ImagenesProductos(models.Model):
    Imagen=models.ImageField(upload_to="productos")
    Codigo=models.ForeignKey(Productos,on_delete=models.CASCADE,related_name="Imagenes")
class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra de {self.producto.nom_producto} por {self.usuario.username}"