import os
from sentence_transformers import SentenceTransformer

# Global cache
_model = None

def get_model():
    global _model
    if _model is None:
        # Load SentenceTransformer model lazily
        _model = SentenceTransformer(
            "paraphrase-multilingual-MiniLM-L12-v2"
        )
    return _model

def get_embedding(text: str):
    return get_model().encode(text)
