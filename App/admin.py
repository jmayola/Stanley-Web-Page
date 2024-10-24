from django.contrib import admin
#--->Traemos la Tablas desde MODELS
from .models import *
from .forms import *
class AdminImagenes(admin.TabularInline):
    model=ImagenesProductos
class AdminProductos(admin.ModelAdmin):
    forms=NuevoProducto
    inlines=[
        AdminImagenes
    ]
# Register your models here.
admin.site.register(Productos,AdminProductos)
admin.site.register(Carrito_detalle)
admin.site.register(Carrito)