
from django.urls import path
from . import views
from .views import ListarNoticiasView, CrearNoticiaView, DetalleNoticiaView, ActualizarNoticiaView, EliminarNoticiaView
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Noticia
from .views import EliminarComentarioView



app_name = 'noticias'

urlpatterns = [
	
	path('', ListarNoticiasView.as_view(), name = 'listar'),
	path('<int:pk>/', DetalleNoticiaView.as_view(), name= 'detalle'),
	path('crear/', CrearNoticiaView.as_view(), name= 'crear_noticias'),
	path('editar/<int:pk>/', ActualizarNoticiaView.as_view(), name='actualizar_noticia'),
	path('eliminar/<int:pk>', EliminarNoticiaView.as_view(), name = 'eliminar_noticias'),
	path('Comentario/', views.Comentar_Noticia, name = 'comentar'),
	path('comentario/eliminar/<int:pk>/', EliminarComentarioView.as_view(), name='eliminar_comentario'),
]