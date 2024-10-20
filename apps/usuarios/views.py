from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegistroForm
from django.views.generic import FormView
from django.contrib.auth import views as auth_views
# Create your views here.

class Registro(CreateView):
	#FORMULARIO DJANGO
	form_class = RegistroForm
	success_url = reverse_lazy('login')
	template_name = 'usuarios/registro.html'

	def form_valid(self,form):
		form.save() 
		return super().form_valid(form)
		
	def register_view(request):
		if request.method == "POST":
			form = SignUpForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('login')
		else:
			form = SingUpForm()
		return render(request, 'usaurios/registro.html', {'form': form})

class Login(auth_views.LoginView):
	template_name = 'usuarios/login.html'

