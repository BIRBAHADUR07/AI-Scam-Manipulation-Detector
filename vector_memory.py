from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorMemory:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # embedding size for all-MiniLM-L6-v2
        self.index = faiss.IndexFlatL2(self.dimension)
        self.messages = []

    def get_embedding(self, text):
        return self.model.encode([text])[0]

    def add_message(self, message):
        embedding = self.get_embedding(message)
        self.index.add(np.array([embedding]).astype('float32'))
        self.messages.append(message)

    def search_similar(self, query, top_k=3):
        if not self.messages:
            return []
        query_embedding = self.get_embedding(query)
        # Search the index
        distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), min(top_k, len(self.messages)))
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                results.append({
                    "message": self.messages[idx],
                    "distance": float(distances[0][i])
                })
        return results
