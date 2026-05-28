# src/agent_ensemble.py
import time
from .preprocessing import TextPreprocessor
from .extraction import InfoExtractor
from .traditional_ml import TraditionalMLClassifier
from .semantic_search import SemanticSearchEngine
from .ollama_client import OllamaOrchestrator
from .RAG_engine import RAGEngine
from .fraud_detection import AuthenticityFraudEngine
from .generator import GroundedProductDescGenerator
from .evaluator import LLMasJudgeEvaluator

class IntellishopEnsembleCoordinator:
    def __init__(self, db_path="data/ecommerce_rag.db", products_json_path="data/products_reviews.json"):
        # 1. Initialize Basic Pipelines
        self.preprocessor = TextPreprocessor()
        self.extractor = InfoExtractor()
        self.traditional_ml = TraditionalMLClassifier()
        self.search_engine = SemanticSearchEngine()
        
        # 2. Initialize Database & RAG
        self.rag_db = RAGEngine(db_path=db_path)
        self.rag_db.populate_database(products_json_path)
        
        # Index all product descriptions for semantic prompt search out-of-the-box
        self.all_products = self.rag_db.get_all_products()
        self.search_engine.index_corpus(self.all_products, text_key="description")
        
        # 3. Initialize Advanced LLMs (Ollama)
        self.ollama = OllamaOrchestrator()
        
        # 4. Initialize Core engines
        self.fraud_engine = AuthenticityFraudEngine(
            traditional_ml_classifier=self.traditional_ml,
            ollama_client=self.ollama
        )
        self.generator = GroundedProductDescGenerator(ollama_client=self.ollama)
        self.judge = LLMasJudgeEvaluator(ollama_client=self.ollama)

    def dynamic_semantic_search(self, natural_language_query, top_k=3):
        """
        Executes semantic matching against products.
        """
        return self.search_engine.search(natural_language_query, top_k=top_k)

    def analyze_single_review(self, review_text, rating, username="", timestamp=None, run_llm=False):
        """
        Ensemble analysis of a single review: preprocessing, aspects extraction, 
        traditional ML baseline sentiment, and deep multi-dimensional fraud checks.
        """
        if not timestamp:
            timestamp = int(time.time())
            
        # Basic: Preprocess
        prep_results = self.preprocessor.process_pipeline(review_text)
        
        # Basic: POS & NER
        extraction_results = self.extractor.process_all(review_text)
        
        # Basic: Traditional Sentiment Score
        traditional_sentiment = self.traditional_ml.predict(review_text)
        traditional_probs = self.traditional_ml.predict_proba(review_text)
        sentiment_label = "Positive" if traditional_sentiment == 1 else "Negative"
        
        # Fetch user review history for burstiness check
        all_reviews = []
        for prod in self.all_products:
            all_reviews.extend(self.rag_db.get_product_reviews(prod["product_id"]))
            
        review_obj = {
            "text": review_text,
            "rating": rating,
            "username": username,
            "timestamp": timestamp
        }
        
        # Advanced: Multi-dimensional Fraud Index
        fraud_metrics = self.fraud_engine.evaluate_fraud_index(review_obj, all_reviews, run_llm=run_llm)
        
        return {
            "preprocessed": prep_results,
            "extracted_features": extraction_results,
            "traditional_ml": {
                "sentiment_label": sentiment_label,
                "positive_confidence": round(traditional_probs[1] * 100, 1),
                "negative_confidence": round(traditional_probs[0] * 100, 1)
            },
            "fraud_analysis": fraud_metrics
        }

    def generate_and_judge_product_description(self, product_id, semantic_query=None):
        """
        Coordinates full RAG-description generation (Gemma) and independent audit (Llama as Judge).
        """
        product = self.rag_db.get_product(product_id)
        if not product:
            return {"error": f"Product {product_id} not found."}
            
        # Retrieve context (grounding reviews)
        context = self.rag_db.retrieve_context_for_rag(
            product_id=product_id,
            query_search_engine=self.search_engine,
            query=semantic_query,
            limit=3
        )
        
        # Generate description using Gemma
        description = self.generator.generate_description(product, context)
        
        # Perform Independent Quality Audit using Llama
        judge_card = self.judge.evaluate_description(product, description)
        
        return {
            "product": product,
            "retrieved_context": context,
            "generated_description": description,
            "scorecard": judge_card
        }
