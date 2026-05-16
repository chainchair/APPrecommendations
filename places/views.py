from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Place
from .ml import recomendar

@login_required
def landing_view(request):
    query = request.GET.get("q", "").strip()
    lugares_recomendados = None
    recomendaciones_por_interes = [] 
    
    # Si hay búsqueda por texto, usar embeddings
    if query:
        try:
            ids = recomendar(query, top_k=20)
            lugares = Place.objects.filter(id__in=ids)
            lugar_dict = {l.pk: l for l in lugares}
            lugares_recomendados = [lugar_dict[id_] for id_ in ids if id_ in lugar_dict]
        except Exception:
            lugares_recomendados = []
    else:
        # Comportamiento original: recomendaciones por intereses
        intereses_usuario = request.user.interests.all()
        
        for interes in intereses_usuario:
            lugares = Place.objects.filter(intereses=interes)[:6]
            if lugares:
                recomendaciones_por_interes.append({
                    'interes': interes,
                    'lugares': lugares
                })
    
    context = {
        'query': query,
        'lugares_recomendados': lugares_recomendados,
        'recomendaciones_por_interes': recomendaciones_por_interes if not query else [],
    }
    
    return render(request, 'places/landing.html', context)

def place_detail_view(request, slug):
    lugar = get_object_or_404(Place, slug=slug)
    context = {
        'lugar': lugar,
    }
    return render(request, 'places/place_detail.html', context)