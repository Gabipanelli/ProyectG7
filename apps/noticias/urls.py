
from django.urls import path
from . import views
from .views import *
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Noticia



app_name = 'noticias'

urlpatterns = [
	
	path('noticia', ListarNoticiasView.as_view(), name = 'listar'),
	path('<int:pk>/', DetalleNoticiaView.as_view(), name= 'detalle'),
	path('noticia/', CrearNoticiaView.as_view(), name= 'crear_noticia'),
	path('editar/<int:pk>/', ActualizarNoticiaView.as_view(), name='actualizar_noticia'),
	path('eliminar/<int:pk>', EliminarNoticiaView.as_view(), name = 'eliminar_noticias'),
	path('Comentario/', views.Comentar_Noticia, name = 'comentar'),
	path('post/categoria/', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('categoria/', CategoriaListView.as_view(), name='categoria_list'),
    path('categoria/<int:pk>/delete/', CategoriaDeleteView.as_view(), name='categoria_delete'),
	path('noticia/<int:pk>/modificar/', NoticiaUpdateView.as_view(), name='noticia_update'),
	path('noticia/<int:pk>/eliminar/', NoticiaDeleteView.as_view(), name='noticia_delete'),
	
]