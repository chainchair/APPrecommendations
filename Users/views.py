from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, InteresesForm
from .models import Interest, CustomUser

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Autenticar y loguear al usuario automáticamente después del registro
            login(request, user)
            # Redirigir a la selección de intereses
            return redirect('seleccion_intereses')
    else:
        form = RegistroForm()
    return render(request, 'users/registro.html', {'form': form})

def seleccion_intereses_view(request):
    # Asegurar que el usuario está logueado
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Si ya tiene intereses seleccionados, redirigir a la página principal o perfil
    if request.user.interests.exists():
        return redirect('inicio')  # Cambia 'inicio' por la URL de tu landing
    
    if request.method == 'POST':
        form = InteresesForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Intereses guardados correctamente!')
            return redirect('inicio')
    else:
        form = InteresesForm(instance=request.user)
    
    # Obtener todos los intereses disponibles para mostrar información adicional si quieres
    todos_intereses = Interest.objects.all()
    return render(request, 'users/seleccion_intereses.html', {
        'form': form,
        'todos_intereses': todos_intereses
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Si el usuario no tiene intereses, redirigir a selección, si no, al inicio
            user_from_db = CustomUser.objects.get(pk=user.pk)
            if not user_from_db.interests.exists():
                return redirect('seleccion_intereses')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('users:login')
