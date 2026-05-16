
from django.shortcuts import render, get_object_or_404
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

def place_detail_view(request, slug):
    lugar = get_object_or_404(Place, slug=slug)
    context = {
        'lugar': lugar,
    }
    return render(request, 'places/place_detail.html', context)