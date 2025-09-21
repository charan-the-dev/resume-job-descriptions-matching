# backend/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle
import os

MODEL_NAME = "all-MiniLM-L6-v2"  # small + fast for hackathon


class EmbedStore:
    def __init__(self, dim=384, index_path="faiss.index", meta_path="meta.pkl"):
        self.model = SentenceTransformer(MODEL_NAME)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.index_path = index_path
        self.meta_path = meta_path
        if os.path.exists(index_path) and os.path.exists(meta_path):
            self.index = faiss.read_index(index_path)
            with open(meta_path, "rb") as f:
                self.meta = pickle.load(f)
        else:
            self.index = faiss.IndexFlatIP(self.dim)  # inner product; will normalize
            self.meta = []  # list of dicts {id, type, ref}

    def embed(self, texts):
        vecs = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        # normalize for cosine similarity
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms[norms == 0] = 1
        vecs = vecs / norms
        return vecs

    def add(self, text, meta):
        vec = self.embed([text])
        self.index.add(vec.astype("float32"))
        self.meta.append(meta)
        self._save()

    def _save(self):
        faiss.write_index(self.index, self.index_path)
        
        import pickle

        with open(self.meta_path, "wb") as f:
            pickle.dump(self.meta, f)

    def query(self, text, top_k=5):
        vec = self.embed([text]).astype("float32")
        D, I = self.index.search(vec, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < len(self.meta):
                results.append((self.meta[idx], float(score)))
        return results
