# this is the vector embeddings service. Takes in list of chunks, returns a list of vectors
# 2 methods meant to embedd texts and querys to later be matched against eachother to give the
# llm the best resources to go off of when answering a question

from sentence_transformers import SentenceTransformer 

MODEL_NAME = "all-MiniLM-L6-v2"   

_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
       _model = SentenceTransformer(MODEL_NAME)
    return _model 

def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()

def embed_query(query: str) -> list[float]:
    return embed_texts([query])[0]