from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Convert a list of text chunks into embedding vectors.
    Each vector has 384 dimensions (fixed by this model).
    """
    embeddings = _model.encode(texts)
    return embeddings.tolist()