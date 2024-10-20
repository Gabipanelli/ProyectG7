from django.urls import path
from .views import Registro
from apps.usuarios import views
from django.contrib.auth import views as auth_views

app_name = 'usuarios'

urlpatterns = [
    
    path('registro/', Registro.as_view(), name = 'registro'),
    path('login/', auth_views.LoginView.as_view(), name = 'login'),

   

]