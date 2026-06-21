# src/semantic_search.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticSearchEngine:
    def __init__(self):
        self.use_transformers = False
        self.model = None
        self.tfidf_vectorizer = None
        self.corpus_vectors = []
        self.items = []
        
        # Try to load SentenceTransformers from local cache only to prevent blocking startup on CDNs
        try:
            from sentence_transformers import SentenceTransformer
            # local_files_only=True forces loading from cache only, avoiding stuck CDN handshakes
            self.model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)
            self.use_transformers = True
            print("Loaded SentenceTransformer ('all-MiniLM-L6-v2') from local cache successfully!")
        except Exception as e:
            print("SentenceTransformer local cache not found or offline. Falling back to robust TF-IDF similarity.")
            self.use_transformers = False
            self.tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1, 2))

    def index_corpus(self, items, text_key="description"):
        """
        Indexes a list of e-commerce items (e.g. products or reviews) for vector search.
        items: list of dicts
        text_key: key in the dict to compute embeddings for
        """
        self.items = items
        texts = [item[text_key] for item in items]
        
        if not texts:
            self.corpus_vectors = []
            return

        if self.use_transformers and self.model:
            try:
                self.corpus_vectors = self.model.encode(texts, show_progress_bar=False)
            except Exception as e:
                print("HuggingFace encoding failed, falling back to TF-IDF. Error:", str(e))
                self.use_transformers = False
                self.tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1, 2))
                self.corpus_vectors = self.tfidf_vectorizer.fit_transform(texts).toarray()
        else:
            self.corpus_vectors = self.tfidf_vectorizer.fit_transform(texts).toarray()

    def search(self, query, top_k=3):
        """
        Computes similarity between query and index, returning top_k matches.
        """
        if len(self.items) == 0:
            return []

        if self.use_transformers and self.model:
            try:
                query_vector = self.model.encode([query], show_progress_bar=False)
                similarities = cosine_similarity(query_vector, self.corpus_vectors)[0]
            except Exception:
                # Naive TF-IDF search fallback if runtime fails
                query_vec = self.tfidf_vectorizer.transform([query]).toarray()
                similarities = cosine_similarity(query_vec, self.corpus_vectors)[0]
        else:
            query_vec = self.tfidf_vectorizer.transform([query]).toarray()
            similarities = cosine_similarity(query_vec, self.corpus_vectors)[0]

        # Rank indices by similarity score descending
        ranked_indices = np.argsort(similarities)[::-1]
        
        results = []
        for i in range(min(top_k, len(ranked_indices))):
            idx = ranked_indices[i]
            results.append({
                "item": self.items[idx],
                "score": float(similarities[idx])
            })
            
        return results
