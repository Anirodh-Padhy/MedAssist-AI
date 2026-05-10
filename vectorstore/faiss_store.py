from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def create_vector_store(chunks):

    # Remove empty chunks
    chunks = [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]

    # Safety check
    if len(chunks) == 0:
        return None, []

    embeddings = model.encode(chunks)

    embeddings = np.array(embeddings)

    # Safety check
    if len(embeddings.shape) < 2:
        return None, []

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index, chunks


def search_vector_store(
    query,
    index,
    chunks,
    top_k=3
):

    if index is None:
        return []

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding),
        top_k
    )

    results = []

    for i in indices[0]:

        if i < len(chunks):
            results.append(chunks[i])

    return results