from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (CreateView, ListView, DetailView, UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from .forms import NoticiaForm, ComentarioForm, NuevaCategoriaForm
from .models import Noticia, Categoria, Comentario
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone

class CrearNoticiaView(CreateView):
	model = Noticia
	form_class = NoticiaForm
	template_name = 'noticias/crear_noticia.html'
	success_url = reverse_lazy('noticias:listar')

class DetalleNoticiaView(DetailView):
    model = Noticia
    context_object_name = 'noticia'
    template_name = 'noticias/detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        noticia = self.object
        comentarios = Comentario.objects.filter(noticia=noticia)
        context['comentarios'] = comentarios
        return context


class ListarNoticiasView(ListView):
    model = Noticia
    template_name = 'noticias/listar.html'
    context_object_name = 'noticias'
    paginate_by = 4 
    




class ActualizarNoticiaView(UpdateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'noticias/form_noticia.html'
    success_url = reverse_lazy('noticias:listar')

    def dispatch(self, request, *args, **kwargs):
        noticia = self.get_object()
        if noticia.usuario != self.request.user:
            raise PermissionDenied("No tienes permiso para editar esta noticia")
        return super().dispatch(request, *args, **kwargs)

#class EliminarNoticiaView(DeleteView):
#    model = Noticia
#    template_name = 'noticias/confirmacion_eliminacion.html'
#    success_url = reverse_lazy('noticias:listar')

#    def dispatch(self, request, *args, **kwargs):
#        noticia = self.get_object()
#        if noticia.usuario != self.request.user:
#            raise PermissionDenied("No tienes permiso para eliminar esta noticia")
#        return super().dispatch(request, *args, **kwargs)

@login_required(login_url='/login/')
def Listar_Noticias(request):
	contexto = {}

	# Parametros de filtro desde la url
	id_categoria = request.GET.get('categoria',None)
	fecha = request.GET.get('fecha',None)
	titulo = request.GET.get('titulo',None)

	# Consulta base
	noticias = Noticia.objects.all()

	#aplicar filtro categoria si existe
	if id_categoria:
		noticias = Noticia.objects.filter(categoria_noticia = id_categoria)
	
	
	# Aplicar filtro fecha si existe
	if fecha == 'asc':
		noticias = noticias.order_by('fecha')
	elif fecha == 'desc':
		noticias = noticias.order_by('-fecha')
	
	# Aplicar filtro por tirulo
	if titulo == 'asc':
		noticias = noticias.order_by('titulo')
	elif titulo == 'desc':
		noticias = noticias.order_by('-titulo')

	contexto['noticias'] = noticias

	# Cargar todas las categorías y autores para los campos de selección
	contexto['categorias'] = Categoria.objects.all().order_by('nombre')

	return render(request, 'noticias/listar.html', contexto)


@login_required
def Detalle_Noticias(request, pk):
    contexto = {}
    try:
        n = Noticia.objects.get(pk=pk)  # Obtienes la noticia con el pk proporcionado.
    except Noticia.DoesNotExist:
        return HttpResponseBadRequest("Noticia no encontrada")

    contexto['noticia'] = n

    # Filtras los comentarios asociados a la noticia usando el campo 'noticia'.
    c = Comentario.objects.filter(noticia=n)
    contexto['comentarios'] = c

    return render(request, 'noticias/detalle.html', contexto)


@login_required
def Comentar_Noticia(request):
    com = request.POST.get('comentario', None)
    usu = request.user
    noti = request.POST.get('id_noticia', None)  # OBTENGO LA PK
    
    # Verificamos si el comentario tiene texto
    if not com:
        return HttpResponseBadRequest('El comentario no puede estar vacío')

    # Intentamos obtener la noticia
    try:
        noticia = Noticia.objects.get(pk=int(noti))
    except Noticia.DoesNotExist:
        return HttpResponseBadRequest('La noticia no existe')

    # Creamos el comentario
    Comentario.objects.create(usuario=usu, noticia=noticia, texto=com)
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
#class NoticiaDetalleView(DetailView):
#    model = Noticia
#   template_name = "noticias/noticia_individual.html"
#    context_object_name = "noticias"
#    pk_url_kwarg = "id"
#    queryset = Noticia.objects.all()

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['form'] = ComentarioForm()
#        context['comentarios'] = self.objects.comentarios.all()
#        return context

#    def noticia(self, request, *args, **kwargs):
#        form = ComentarioForm(request.POST)
#        if form.is_valid():
#            comentario = form.save(commit=False)
#            comentario.usuario = request.user
#            comentario.noticia_id = self.kwargs['id']
#            comentario.save()
#            return redirect('apps.noticias.noticia_individual', id=self.kwargs['id'])
#        else:
#            context = self.get_context_data(**kwargs)
#            context['form'] = form
#            return self.render_to_response(context)


class NoticiaCreateView(CreateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'noticias/crear_noticia.html'
    success_url = reverse_lazy('noticias:listar')

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = NuevaCategoriaForm
    template_name = 'noticias/crear_categoria.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('noticias:crear_noticia')


class CategoriaListView(ListView):
    model = Categoria
    template_name = 'noticias/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'noticias/categoria_delete.html'
    success_url = reverse_lazy('noticias:categoria_list')


class ModificarNoticiaView(LoginRequiredMixin, UpdateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'noticias/modificar_noticia.html'
    success_url = reverse_lazy('noticias:listar')

class EliminarNoticiaView(DeleteView):
    model = Noticia
    template_name = 'noticias/eliminar_noticia.html'
    success_url = reverse_lazy('noticias:listar')

class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'noticias/crear_comentario.html'
    success_url = 'noticias/comentar/'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.posts_id = self.kwargs['noticia_id']
        return super().form_valid(form)
class ComentarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'noticias/comentario_form.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('noticias:noticia_individual', args=[self.object.noticia.id])

class ComentarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'noticias/eliminar_comentario.html'

    def get_success_url(self):
        return reverse('noticias:detalle', args=[self.object.noticia.id])


class NoticiaPorCategoriaView(ListView):
    model = Noticia 
    template_name = 'noticias/noticia_por_categoria.html'
    context_object_name = 'noticias'

    def get_queryset(self):
        return Noticia.objects.filter(categoria_id=self.kwargs['pk'])