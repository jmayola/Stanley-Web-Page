from django.db import models
from ckeditor import fields
from django.contrib.auth.models import User
# Create your models here.
class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nom_producto = models.TextField(max_length=50, null=False)
    desc_producto = fields.RichTextField(null=True)
    precio_producto = models.IntegerField(null=False)
    precioreb_producto = models.IntegerField(null=True)
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
        return self.carrito_det
class ImagenesProductos(models.Model):
    Imagen=models.ImageField(upload_to="productos")
    Codigo=models.ForeignKey(Productos,on_delete=models.CASCADE,related_name="Imagenes")