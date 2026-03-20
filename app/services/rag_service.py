import os
from dotenv import load_dotenv

from google import genai
from app.services.embedding_service import embed_query
from app.vector_store import get_collection

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_question(question: str) -> str:
    query_vector = embed_query(question)
    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=5
    )
    
    chunks = results["documents"][0]
    context = "\n\n".join(chunks)
    
    prompt = f"""You are a research assistant. Use only the context below to answer the question.
    If the answer cannot be found in the context, say "I don't have enough information to answer that."

    Context:
    {context}

    Question: {question}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text
    