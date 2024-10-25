from django.shortcuts import render
from django.views.generic import (CreateView, ListView, DetailView, UpdateView, DeleteView)
from django.urls import reverse_lazy
from .forms import RegistroForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib import messages
from .models import Usuario
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

# Vista basada en clase para el registro
class RegistrarUsuario(CreateView):
    template_name = 'usuarios/registro.html'
    form_class = RegistroForm
    success_url = reverse_lazy('usuarios:login')  # Cambiado a 'usuarios:login' para usar el namespace correcto

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registro exitoso. Por favor, inicia sesión.')
        group = Group.objects.get(name='Registrado')
        self.object.groups.add(group)
        return redirect('usuarios:login')

# Vista basada en clase para el login
class Login(auth_views.LoginView):
    template_name = 'usuarios/login.html'

class LogoutUsuario(auth_views.LogoutView):
    template_name = 'usuarios/logout.html'

    def get_sussces_url(self):
        messages.success(self.request, 'logout exitoso')
        
        return reverse('apps.usuarios:logout')

class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios/listar_usuario.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(is_superuser=True)
        return queryset


class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/eliminar_usuario.html'
    success_url = reverse_lazy('usuarios:listar_usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colaborador_group = Group.objects.get(name='Colaborador')
        es_colaborador = colaborador_group in self.object.groups.all()
        context['es_colaborador'] = es_colaborador
        return context

    def post(self, request, *args, **kwargs):
        eliminar_comentario = request.POST.get('eliminar_comentario', False)
        eliminar_noticia = request.POST.get('eliminar_noticia', False)
        self.object = self.get_object()
        if eliminar_comentario:
            Comentario.objects.filter(usuario=self.object).delete()
        if eliminar_noticia:
            Post.objects.filter(autor=self.object).delete()
        messages.success(request, f'Usuario {self.object.username} eliminado correctamente')
        return self.delete(request, *args, **kwargs)