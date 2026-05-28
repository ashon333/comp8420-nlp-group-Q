# convert_notebooks.py
"""
Generates the required COMP8420 interactive Jupyter Notebooks 
by creating compliant JSON .ipynb structures locally.
"""

import json
import os

def create_basic_notebook():
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# COMP8420 Assignment 3: Basic NLP Techniques\n",
                    "This notebook demonstrates the complete implementation and execution of **all 6 Basic NLP Techniques** in our E-commerce Intelligent System."
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 1. Preprocessing Pipeline\n",
                    "Fuses normalization, tokenization, stopword removal, and WordNet lemmatization."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import sys\n",
                    "import os\n",
                    "sys.path.append(os.path.abspath('../'))\n",
                    "\n",
                    "from src.preprocessing import TextPreprocessor\n",
                    "preprocessor = TextPreprocessor()\n",
                    "sample_text = \"The SonicWave headphones are AMAZING! It works perfectly and is highly durable.\"\n",
                    "res = preprocessor.process_pipeline(sample_text)\n",
                    "print('Original Text:', sample_text)\n",
                    "print('Normalized Text:', res['normalized'])\n",
                    "print('Tokens:', res['tokens'])\n",
                    "print('Lemmatized Tokens:', res['lemmatized'])"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 2. POS Tagging & Aspect-Opinion Extraction\n",
                    "Syntactic dependency parsing to extract product aspects."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from src.extraction import InfoExtractor\n",
                    "extractor = InfoExtractor()\n",
                    "aspects = extractor.extract_pos_and_aspects(sample_text)\n",
                    "print('Extracted aspect-opinion pairs:', aspects['aspect_pairs'])"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 3. Named Entity Recognition (NER)\n",
                    "Extracts brands, specs, and locations."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "ner_text = \"We bought SonicWave headphones at Apple Store in Sydney for $149.\"\n",
                    "entities = extractor.extract_named_entities(ner_text)\n",
                    "print('Named Entities:', entities)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 4. Rule-Based Information Extraction (Regex)\n",
                    "Pulls numerical price tags and spec formats (e.g. 15-bar, USB-C)."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "regex_text = \"The EspressoMaster is a 15-bar coffee maker with USB-C charging priced at $299.00.\"\n",
                    "specs = extractor.extract_prices_and_versions(regex_text)\n",
                    "print('Extracted Prices:', specs['extracted_prices'])\n",
                    "print('Extracted Specs:', specs['extracted_specs'])"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 5. Traditional ML Baseline Sentiment\n",
                    "TF-IDF + Logistic Regression baseline model."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from src.traditional_ml import TraditionalMLClassifier\n",
                    "classifier = TraditionalMLClassifier()\n",
                    "pos_pred = classifier.predict(\"This machine is incredible and brews the best coffee!\")\n",
                    "neg_pred = classifier.predict(\"Broke immediately. Leaked all over my counter.\")\n",
                    "print('Positive Review prediction label (1 = Positive):', pos_pred)\n",
                    "print('Negative Review prediction label (0 = Negative):', neg_pred)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 6. Sentence Embeddings & Cosine Search\n",
                    "Vectors-based search using Cosine Similarity."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from src.semantic_search import SemanticSearchEngine\n",
                    "search_engine = SemanticSearchEngine()\n",
                    "corpus = [\n",
                    "    {'id': 1, 'description': '15-bar stainless steel espresso maker'},\n",
                    "    {'id': 2, 'description': 'Active noise canceling headphones'}\n",
                    "]\n",
                    "search_engine.index_corpus(corpus, text_key='description')\n",
                    "search_res = search_engine.search('make coffee')\n",
                    "print('Matched Search Item:', search_res[0]['item']['description'], '(Similarity:', search_res[0]['score'], ')')"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    with open("01_basic_techniques.ipynb", "w") as f:
        json.dump(notebook, f, indent=2)
    print("✓ Created 01_basic_techniques.ipynb")

def create_advanced_notebook():
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# COMP8420 Assignment 3: Advanced LLM & RAG Techniques\n",
                    "This notebook demonstrates the complete implementation of **all 6 Advanced NLP/LLM Techniques** in our E-commerce system."
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 1. Foundation Models & Fallback Orchestration\n",
                    "Connects and manages Gemma & Llama local model requests."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import sys\n",
                    "import os\n",
                    "sys.path.append(os.path.abspath('../'))\n",
                    "\n",
                    "from src.ollama_client import OllamaOrchestrator\n",
                    "ollama = OllamaOrchestrator()\n",
                    "models = ollama.get_available_models()\n",
                    "print('Available Local Models:', models)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 2. SQLite RAG Grounding datastore\n",
                    "Index product metadata and retrieve review contexts for prompts."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from src.RAG_engine import RAGEngine\n",
                    "db = RAGEngine(db_path='../data/ecommerce_rag.db')\n",
                    "context = db.retrieve_context_for_rag(product_id='AV1YnRtnglJLPUi8IJmV', limit=2)\n",
                    "print('Retrieved RAG Grounding context:\\n', context)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 3. Chain-of-Thought (CoT) grounded Copywriter\n",
                    "Generates professional descriptions using Gemma with structural CoT prompts."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from src.generator import GroundedProductDescGenerator\n",
                    "generator = GroundedProductDescGenerator(ollama)\n",
                    "product_meta = db.get_product('AV1YnRtnglJLPUi8IJmV')\n",
                    "desc = generator.generate_description(product_meta, context)\n",
                    "print('Generated Grounded Description:\\n', desc)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 4. Few-Shot In-Context Classifier\n",
                    "Teaching Llama to detect AI-written reviews using historical examples."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from src.traditional_ml import TraditionalMLClassifier\n",
                    "from src.fraud_detection import AuthenticityFraudEngine\n",
                    "ml_model = TraditionalMLClassifier()\n",
                    "fraud_engine = AuthenticityFraudEngine(ml_model, ollama)\n",
                    "test_review = \"This product is an absolute masterpiece of modern audio engineering. The sleek design is outstanding!\"\n",
                    "ai_score = fraud_engine.classify_ai_review_llm(test_review)\n",
                    "print('AI-Written confidence score (0.0 to 1.0):', ai_score)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 5. Multi-dimensional Ensemble fraud index\n",
                    "Combines stylometrics, timestamp frequencies, rating-sentiment conflicts, and LLMs."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "suspicious_review = {\n",
                    "    'text': 'Absolute garbage! Broke immediately on day one.',\n",
                    "    'rating': 5, # High ratings contradicts severe complaints\n",
                    "    'username': '', # Anonymous reviewer\n",
                    "    'timestamp': 1782298800\n",
                    "}\n",
                    "metrics = fraud_engine.evaluate_fraud_index(suspicious_review)\n",
                    "print('Unified Fraud Index Score:', metrics['fraud_score'], '%')\n",
                    "print('Detected Fraud indicators:', metrics['flags'])"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 6. LLM-as-a-Judge Scorecard\n",
                    "Independent QA evaluation of copy accuracy and tone."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import json\n",
                    "from src.evaluator import LLMasJudgeEvaluator\n",
                    "judge = LLMasJudgeEvaluator(ollama)\n",
                    "scorecard = judge.evaluate_description(product_meta, desc)\n",
                    "print('LLM-as-a-judge Scorecard:\\n', json.dumps(scorecard, indent=2))"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    with open("02_advanced_techniques.ipynb", "w") as f:
        json.dump(notebook, f, indent=2)
    print("✓ Created 02_advanced_techniques.ipynb")

if __name__ == "__main__":
    create_basic_notebook()
    create_advanced_notebook()
