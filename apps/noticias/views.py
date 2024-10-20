from django.shortcuts import render, redirect
from django.views.generic import (CreateView, ListView, DetailView, UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from .forms import NoticiaForm
from .models import Noticia, Categoria, Comentario
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy

class CrearNoticiaView(CreateView):
	model = Noticia
	form_class = NoticiaForm
	template_name = 'noticias/form_noticia.html'
	success_url = reverse_lazy('lista_noticias')

class DetalleNoticiaView(DetailView):
	model = Noticia
	context_object_name = 'noticia'
	template_name = 'noticias/detalle.html'

class ListarNoticiasView(ListView):
	model = Noticia
	template_name = 'noticias/listar.html'
	context_object_name = 'noticias'
	paginate_by = 4 
	
	def get_queryset(self):
		query = self.request.GET.get('titulo')
		queryset = super().get_queryset()  
		if query:
			queryset = queryset.filter(titulo__icontains=query)
		return queryset.order_by('titulo')

class ActualizarNoticiaView(UpdateView):
	model = Noticia
	form_class = NoticiaForm
	template_name = 'noticias/form_noticia.html'
	success_url = reverse_lazy('lista_noticias')

class EliminarNoticiaView(DeleteView):
	model = Noticia
	template_name = 'noticias/confirmacion_eliminacion.html'
	success_url = reverse_lazy('lista_noticias')

@login_required
def Listar_Noticias(request):
	contexto = {}

	id_categoria = request.GET.get('id',None)

	if id_categoria:
		n = Noticia.objects.filter(categoria_noticia = id_categoria)
	else:
		n = Noticia.objects.all() #RETORNA UNA LISTA DE OBJETOS

	contexto['noticias'] = n

	cat = Categoria.objects.all().order_by('nombre')
	contexto['categorias'] = cat

	return render(request, 'noticias/listar.html', contexto)

@login_required
def Detalle_Noticias(request, pk):
	contexto = {}
	try:
		n = Noticia.objects.get(pk=pk)
	except Noticia.DoesNotExist:
		return HttpResponseBadRequest("Noticia no encontrada")

	n = Noticia.objects.get(pk = pk) #RETORNA SOLO UN OBEJTO
	contexto['noticia'] = n

	c = Comentario.objects.filter(noticia = n)
	contexto['comentarios'] = c

	return render(request, 'noticias/detalle.html',contexto)


@login_required
def Comentar_Noticia(request):
	com = request.POST.get('comentario',None)
	usu = request.user
	noti = request.POST.get('id_noticia', None)# OBTENGO LA PK
	try:
		noticia = Noticia.objects.get(pk=int(noti))
	except Noticia.DoesNotExist:
		return HttpResponseBadRequest('La noticia no existe')

	noticia = Noticia.objects.get(pk = noti) #BUSCO LA NOTICIA CON ESA PK
	coment = Comentario.objects.create(usuario = usu, noticia = noticia, texto = com)
	return redirect(reverse_lazy('noticias:detalle', kwargs={'pk': noti}))

#{'nombre':'name', 'apellido':'last name', 'edad':23}
#EN EL TEMPLATE SE RECIBE UNA VARIABLE SEPARADA POR CADA CLAVE VALOR
# nombre
# apellido
# edad

'''
ORM

CLASE.objects.get(pk = ____)
CLASE.objects.filter(campos = ____)
CLASE.objects.all() ---> SELECT * FROM CLASE

'''