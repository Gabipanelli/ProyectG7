from django.db import models
from .models import Noticia
from django import forms

class NoticiaForm(forms.ModelForm):
    class Meta: 
        model = Noticia
        fields = ['titulo', 'cuerpo', 'imagen','categoria_noticia', 'descripcion', 'ubicacion']
        widges = {
            'fecha': forms.DateInput(attrs= {'tipe':'date'}),
        }
    