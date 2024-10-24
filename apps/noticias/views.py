from django.shortcuts import render, redirect, get_object_or_404
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
    queryset = Noticia.objects.all()

    fecha_inicio = self.request.GET.get('fecha_inicio')
    fecha_fin = self.request.GET.get('fecha_fin')
    comentarios_min = self.request.GET.get('comentarios_min')

    if fecha_inicio and fecha_fin:
        queryset = queryset.filter(fecha__range=[fecha_inicio, fecha_fin])

    if comentarios_min:
        queryset = queryset.annotate(num_comentarios=models.Count('comentario')).filter(num_comentarios__gte=comentarios_min)

    return queryset

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

class EliminarNoticiaView(DeleteView):
    model = Noticia
    template_name = 'noticias/confirmacion_eliminacion.html'
    success_url = reverse_lazy('noticias:listar')

    def dispatch(self, request, *args, **kwargs):
        noticia = self.get_object()
        if noticia.usuario != self.request.user:
            raise PermissionDenied("No tienes permiso para eliminar esta noticia")
        return super().dispatch(request, *args, **kwargs)

@login_required(login_url='/login/')
def listar_noticias(request):
    contexto = {}

    id_categoria = request.GET.get('id', None)

    if id_categoria:
        try:
            # Verifica si el id_categoria es un número antes de hacer la consulta
            id_categoria = int(id_categoria)
            n = Noticia.objects.filter(categoria_noticia=id_categoria)
        except ValueError:
            # Si no es un número, devolver todas las noticias
            n = Noticia.objects.all()
    else:
        n = Noticia.objects.all()  # RETORNA UNA LISTA DE OBJETOS

    contexto['noticias'] = n

    # Obtener todas las categorías y ordenarlas por nombre
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


# Vista para editar un comentario
class EditarComentarioView(UpdateView):
    model = Comentario
    fields = ['texto']
    template_name = 'comentarios/editar_comentario.html'

    def get_success_url(self):
        noticia_id = self.object.noticia.id
        return reverse_lazy('detalle_noticia', kwargs={'pk': noticia_id})

    # Verificar que el usuario es el propietario del comentario
    def dispatch(self, request, *args, **kwargs):
        comentario = self.get_object()
        if comentario.usuario != self.request.user:
            return HttpResponseForbidden('No tienes permiso para editar este comentario.')
        return super().dispatch(request, *args, **kwargs)


class EliminarComentarioView(DeleteView):
    model = Comentario
    template_name = 'comentarios/eliminar_comentarios.html'

    def get_success_url(self):
        noticia_id = self.object.noticia.id
        return reverse_lazy('detalle_noticia', kwargs={'pk': noticia_id})

    # Verificar que el usuario es el propietario del comentario
    def dispatch(self, request, *args, **kwargs):
        comentario = self.get_object()
        if comentario.usuario != self.request.user:
            return HttpResponseForbidden('No tienes permiso para eliminar este comentario.')
        return super().dispatch(request, *args, **kwargs)


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