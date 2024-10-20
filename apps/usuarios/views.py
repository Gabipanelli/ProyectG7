from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegistroForm
from django.contrib.auth import views as auth_views

# Vista basada en clase para el registro
class Registro(CreateView):
    form_class = RegistroForm
    success_url = reverse_lazy('usuarios:login')  # Cambiado a 'usuarios:login' para usar el namespace correcto
    template_name = 'usuarios/registro.html'

    def form_valid(self, form):
        form.save()  # Guarda el usuario
        return super().form_valid(form)

# Vista basada en clase para el login
class Login(auth_views.LoginView):
    template_name = 'usuarios/login.html'