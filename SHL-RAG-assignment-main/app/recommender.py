import json
import numpy as np
import faiss
from app.models.embedder import get_embedding

def recommend_query(query):
    with open("data/shl_assessments.json", "r") as f:
        assessments = json.load(f)

    query_vector = np.array([get_embedding(query)], dtype="float32")
    index = faiss.read_index("data/vectors.index")
    D, I = index.search(query_vector, 5)

    return [assessments[i] for i in I[0] if i < len(assessments)]
