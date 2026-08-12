from sentence_transformers import SentenceTransformer

# Load once (global)
# model = SentenceTransformer("all-MiniLM-L6-v2")

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

def get_embedding(text: str):
    return model.encode(text)

