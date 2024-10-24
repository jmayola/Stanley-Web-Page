#---> Importamos 'FORMS'
from django import forms
#---> Importamos los Modelos/Tablas
from .models import *

class NuevoProducto(forms.ModelForm):
    class Meta:
        model = Productos
        fields = '__all__'  # Esto incluirá todos los campos del modelo Productos

# ---> Formulario de registro extendido
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )  # Campos que quieres incluir en el registro
