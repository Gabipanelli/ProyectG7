from django.db import models
from .models import Noticia
from django import forms
from .models import Comentario, Noticia, Categoria

class NoticiaForm(forms.ModelForm):
    class Meta: 
        model = Noticia
        fields = ['titulo', 'cuerpo', 'imagen','categoria_noticia', 'descripcion', 'ubicacion']
        widges = {
            'fecha': forms.DateInput(attrs= {'tipe':'date'}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta: 
        modell = Comentario
        fields = ['texto']

class NuevaCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'