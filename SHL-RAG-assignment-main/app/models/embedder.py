import os
import cohere

co = cohere.Client(os.getenv("COAPI_KEY"))

def get_embedding(text):
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings[0]
