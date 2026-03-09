import time
from vector_memory import VectorMemory

class SynrixMemoryEngine:
    def __init__(self):
        # We simulate the lattice nodes using a list of dictionaries
        # Each message node stores sender, timestamp, the text, classification & risk_score
        self.lattice = []
        self.vector_store = VectorMemory()

    def add_message(self, sender, text, risk_score=None, classification=None):
        node = {
            "id": len(self.lattice),
            "sender": sender,
            "text": text,
            "timestamp": time.time(),
            "risk_score": risk_score,
            "classification": classification
        }
        self.lattice.append(node)
        self.vector_store.add_message(text)
        return node["id"]

    def update_message_analysis(self, msg_id, risk_score, classification):
        if 0 <= msg_id < len(self.lattice):
            self.lattice[msg_id]['risk_score'] = risk_score
            self.lattice[msg_id]['classification'] = classification

    def get_recent_context(self, limit=3):
        return self.lattice[-limit:] if self.lattice else []

    def search_similar_messages(self, query_text):
        return self.vector_store.search_similar(query_text)
