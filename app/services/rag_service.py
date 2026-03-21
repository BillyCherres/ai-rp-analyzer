# This is our rag service 
# a service that establishes a connection with the gemini llm. 
# its meant to act as a pipeline that enhances the llms answers. 
# takes in a question and uses sentence transformers to convert it as a vector
# The chromadb handles the matching of the question vector, and its relavent chunked vectors
# Then based off these results, the llm is meant to give a more meaningful answer now 
# that it has the relavent data to go off of


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
    