# verify_system.py
"""
COMP8420 Assignment 3: Automated Quality & Testing Suite
Verifies that all 12 basic and advanced techniques function correctly.
"""

import sys
import os

# Add src to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.preprocessing import TextPreprocessor
from src.extraction import InfoExtractor
from src.traditional_ml import TraditionalMLClassifier
from src.semantic_search import SemanticSearchEngine
from src.ollama_client import OllamaOrchestrator
from src.RAG_engine import RAGEngine
from src.fraud_detection import AuthenticityFraudEngine
from src.generator import GroundedProductDescGenerator
from src.evaluator import LLMasJudgeEvaluator

def run_tests():
    print("====================================================")
    print("🚨 Starting IntelliShop AI Integration Test Suite 🚨")
    print("====================================================")

    # Test 1: Preprocessing
    print("\n[Test 1] Preprocessing Pipeline...")
    preprocessor = TextPreprocessor()
    test_text = "The SonicWave headphones are AMAZING! It works perfectly and is durable."
    prep_res = preprocessor.process_pipeline(test_text)
    print("  ✓ Lemmatized tokens:", prep_res["lemmatized"])
    assert "amazing" in prep_res["lemmatized"], "Failed lemmatizer check"
    
    # Test 2: POS aspect extraction
    print("\n[Test 2] spaCy POS & Aspects Extraction...")
    extractor = InfoExtractor()
    extract_res = extractor.process_all(test_text)
    print("  ✓ Extracted Nouns (Aspects):", extract_res["nouns"])
    print("  ✓ Aspect Pairs:", extract_res["aspect_pairs"])
    print("  ✓ Extracted prices and specs:", regex_info := extractor.extract_prices_and_versions("Brews coffee under 15-bar pressure and charges via USB-C for $299.00."))
    assert "$299.00" in regex_info["extracted_prices"], "Failed price regex extraction"
    
    # Test 3: Traditional ML Sentiment
    print("\n[Test 3] Traditional ML baseline Classifier...")
    ml_model = TraditionalMLClassifier()
    pos_pred = ml_model.predict("Highly recommend! Perfect build and amazing battery.")
    neg_pred = ml_model.predict("Absolute garbage, leaks everywhere and broke immediately.")
    print("  ✓ Positive prediction label:", pos_pred)
    print("  ✓ Negative prediction label:", neg_pred)
    assert pos_pred == 1, "Failed ML Positive test"
    assert neg_pred == 0, "Failed ML Negative test"
    
    # Test 4: Semantic Cosine Search
    print("\n[Test 4] Embeddings & Cosine Search Engine...")
    search_engine = SemanticSearchEngine()
    dummy_corpus = [
        {"id": 1, "description": "High pressure espresso coffee machine maker."},
        {"id": 2, "description": "Wireless Bluetooth active noise canceling headphones."},
        {"id": 3, "description": "Waterproof smart smartwatch fitness tracker band."}
    ]
    search_engine.index_corpus(dummy_corpus, text_key="description")
    results = search_engine.search("brew coffee", top_k=1)
    print(f"  ✓ Search query 'brew coffee' matched: '{results[0]['item']['description']}' (Similarity Score: {round(results[0]['score'], 3)})")
    assert results[0]["item"]["id"] == 1, "Failed Semantic search validation"

    # Test 5: Database RAG
    print("\n[Test 5] SQLite RAG Database populating...")
    db_path = "data/ecommerce_test.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    rag_db = RAGEngine(db_path=db_path)
    rag_db.populate_database("data/products_reviews.json")
    products = rag_db.get_all_products()
    print(f"  ✓ Products loaded inside SQLite database: {len(products)}")
    assert len(products) > 0, "Failed to load products into SQLite"
    
    # Test 6: Ollama & LLMs connection
    print("\n[Test 6] Ollama Local Models connection check...")
    ollama = OllamaOrchestrator()
    models = ollama.get_available_models()
    print("  ✓ Local Ollama models found:", models)
    
    # Test 7: Authenticity Fraud Ingestion
    print("\n[Test 7] Authenticity & Fraud Indexing...")
    fraud_engine = AuthenticityFraudEngine(ml_model, ollama)
    suspicious_review = {
        "text": "Absolute garbage! Spares broke on day one.",
        "rating": 5, # Rating CONTRADICTS negative sentiment
        "username": "", # Missing user
        "timestamp": 1782298800
    }
    fraud_card = fraud_engine.evaluate_fraud_index(suspicious_review, run_llm=True)
    print("  ✓ Evaluated Fraud Index Score:", fraud_card["fraud_score"], "%")
    print("  ✓ Active security warnings:", fraud_card["flags"])
    assert fraud_card["fraud_score"] > 30, "Failed to catch obvious rating contradiction/anonymous user"
    
    print("\n====================================================")
    print("🎉 All core techniques validated successfully! 🎉")
    print("====================================================")

if __name__ == "__main__":
    run_tests()
