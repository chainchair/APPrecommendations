import os
import django
from django.conf import settings
from django.core.files import File
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebRecomendaciones.settings')  # Cambia 'tu_proyecto' por el nombre de tu proyecto
django.setup()

from places.models import Place, Category  # Cambia 'tu_app' por el nombre de tu app

def fill_missing_photos():
    """
    Rellena las fotos faltantes de los lugares según su categoría.
    Busca fotos en media/places/ con nombre: {categoria_en_minusculas}.jpg/.png
    """
    
    # Obtener todos los lugares sin foto
    lugares_sin_foto = Place.objects.filter(imagen='')
    
    if not lugares_sin_foto.exists():
        print("✅ No hay lugares sin foto.")
        return
    
    print(f"📸 Procesando {lugares_sin_foto.count()} lugares sin foto...")
    
    # Contadores para reporte
    actualizados = 0
    no_encontradas = 0
    
    for lugar in lugares_sin_foto:
        if not lugar.categoria:
            print(f"⚠️  Lugar '{lugar.nombre}' - Sin categoría asignada, se omite")
            no_encontradas += 1
            continue
        
        # Obtener nombre de la categoría en minúsculas
        nombre_categoria = lugar.categoria.name.lower()
        
        # Posibles extensiones de imagen
        extensiones = ['.jpg','png', '.jpeg', '.png', '.webp']
        ruta_foto = None
        
        # Buscar la foto por categoría en media/places/
        media_places_path = Path(settings.MEDIA_ROOT) / 'places'
        
        for ext in extensiones:
            nombre_archivo = f"{nombre_categoria}{ext}"
            ruta_completa = media_places_path / nombre_archivo
            
            if ruta_completa.exists():
                ruta_foto = ruta_completa
                break
        
        if ruta_foto:
            # Abrir el archivo y asignarlo al lugar
            with open(ruta_foto, 'rb') as f:
                lugar.imagen.save(f"{nombre_categoria}{ruta_foto.suffix}", File(f), save=True)
            
            print(f"✅ Lugar '{lugar.nombre}' - Asignada foto de categoría: {nombre_categoria}")
            actualizados += 1
        else:
            print(f"❌ Lugar '{lugar.nombre}' - No se encontró foto para categoría: {nombre_categoria}")
            no_encontradas += 1
    
    # Reporte final
    print("\n" + "="*50)
    print(f"📊 REPORTE FINAL:")
    print(f"   ✅ Actualizados: {actualizados}")
    print(f"   ❌ Sin foto disponible: {no_encontradas}")
    print(f"   📍 Total procesados: {actualizados + no_encontradas}")
    print("="*50)

def verificar_fotos_disponibles():
    """Función opcional para ver qué fotos por categoría existen"""
    media_places_path = Path(settings.MEDIA_ROOT) / 'places'
    
    if not media_places_path.exists():
        print(f"❌ La carpeta {media_places_path} no existe")
        return
    
    # Obtener todas las categorías
    categorias = Category.objects.all()
    
    print("📋 FOTOS DISPONIBLES POR CATEGORÍA:")
    print("-" * 40)
    
    for cat in categorias:
        nombre_cat = cat.name.lower()
        encontrada = False
        
        for ext in ['.jpg', '.jpeg', '.png', '.webp']:
            if (media_places_path / f"{nombre_cat}{ext}").exists():
                encontrada = True
                break
        
        estado = "✅" if encontrada else "❌"
        print(f"{estado} {cat.name} -> {nombre_cat}.jpg/.png/.webp")
    
    print("-" * 40)

if __name__ == "__main__":
    print("¿Qué deseas hacer?")
    print("1. Verificar qué fotos están disponibles por categoría")
    print("2. Rellenar fotos faltantes")
    
    opcion = input("\nElige opción (1 o 2): ").strip()
    
    if opcion == "1":
        verificar_fotos_disponibles()
    elif opcion == "2":
        confirmar = input("¿Estás seguro de rellenar las fotos? (s/n): ").strip().lower()
        if confirmar == 's':
            fill_missing_photos()
        else:
            print("Operación cancelada.")
    else:
        print("Opción no válida.")
