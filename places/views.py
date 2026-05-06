from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Place

@login_required
def landing_view(request):
    # Obtener los intereses del usuario logueado
    intereses_usuario = request.user.interests.all()
    
    # Crear un diccionario donde cada interés tiene su lista de lugares
    recomendaciones_por_interes = []
    
    for interes in intereses_usuario:
        lugares = Place.objects.filter(intereses=interes)[:6]  # Máximo 6 lugares por interés
        if lugares:
            recomendaciones_por_interes.append({
                'interes': interes,
                'lugares': lugares
            })
    
    context = {
        'recomendaciones_por_interes': recomendaciones_por_interes,
    }
    
    return render(request, 'places/landing.html', context)