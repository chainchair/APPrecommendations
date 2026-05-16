import numpy as np
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Rutas relativas a este archivo
BASE_DIR = Path(__file__).resolve().parent

# Carga perezosa (se ejecuta al importar el módulo)
_model = None
_embeddings = None
_ids = None

def _load():
    global _model, _embeddings, _ids
    
    if _model is None:
        _model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    if _embeddings is None:
        _embeddings = np.load(BASE_DIR / "embeddings.npy")
    
    if _ids is None:
        with open(BASE_DIR / "ids.json", "r") as f:
            _ids = json.load(f)

def recomendar(texto, top_k=10):
    """
    Recibe texto del usuario, retorna lista de IDs de Place ordenados por similitud.
    """
    _load()
    
    # Generar embedding de la consulta
    query_vec = _model.encode([texto])  # (1, 384)# type: ignore
    if hasattr(query_vec, 'numpy'):
        query_vec = query_vec.numpy()
        
    query_vec = np.asarray(query_vec, dtype=np.float32)
    
    # 4. Asegurar que _embeddings no es None
    if _embeddings is None:
        return []
    
    # Calcular similitud coseno
    similitudes = cosine_similarity(query_vec, _embeddings)[0]  # (250,)
    
    top_indices = np.argsort(similitudes)[::-1][:top_k]
    if _ids is None:
        return []
    
    # Obtener índices ordenados por mayor similitud
    
    
    # Mapear índices a IDs reales
    ids_recomendados = [_ids[i] for i in top_indices]
    
    return ids_recomendados