from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegistroForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib import messages
from django.shortcuts import redirect

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

