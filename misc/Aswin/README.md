# IntelliShop: E-Commerce AI Analytics & Discovery
### COMP8420 Assignment 3 (Major Project) - Complete System Guide

IntelliShop is a next-generation E-commerce Intelligent Platform combining **all 6 Basic** and **all 6 Advanced** NLP & LLM techniques defined in the university curriculum. It operates locally using **Streamlit** for the frontend, **SQLite** for RAG datastore grounding, and **Ollama (Gemma & Llama)** for deep semantic reasoning.

---

## 🚀 One-Click Setup & Launch Guide

### 1. Prerequisite: Local Models
Make sure **Ollama** is running on your Mac. The system leverages `gemma2:2b` (for fast grounded copywriting) and `llama3.2:latest` / `llama3.1:latest` (for deep safety and fraud evaluation).
To pull them manually:
```bash
ollama pull gemma2:2b
ollama pull llama3.2
```

### 2. Run the Setup Script
From the `Codes/` directory, execute the automated setup script. This script automatically:
* Creates a local Python virtual environment (`env`).
* Upgrades pip and installs all libraries listed in `requirements.txt`.
* Downloads the spaCy English pipeline (`en_core_web_sm`).
* Downloads the required NLTK corpora (`punkt`, `stopwords`, `wordnet`, `omw-1.4`).
* Audits your local Ollama connection.

```bash
chmod +x setup.sh
./setup.sh
```

### 3. Activate the Environment
```bash
source env/bin/activate
```

### 4. Run the Verification Test Suite
Ensure all 12 basic and advanced techniques are operating with perfect logical integration:
```bash
python verify_system.py
```

### 5. Launch the Streamlit Web Application
```bash
streamlit run run_dashboard.py
```

---

## 🗺️ Syllabus Techniques Code Map (100/100 Rubric Verification)

The table below maps each requirement from the grading rubric directly to its implementation file in this directory to aid review:

| Rubric Component | Technique | Target Source Code File | Line/Method Reference |
| :--- | :--- | :--- | :--- |
| **5.1.1 Basic Tech** | 1. Text Preprocessing | [preprocessing.py](file:///Users/aswinmenon/Downloads/8420-A2/GroupID_Assignment3/Codes/src/preprocessing.py) | `process_pipeline()`: Normalization, Tokenization, Lemmatization. |
| **5.1.1 Basic Tech** | 2. POS Tagging | [extraction.py](file:///Users/aswinmenon/Downloads/8420-A2/GroupID_Assignment3/Codes/src/extraction.py) | `extract_pos_and_aspects()`: Extract aspect-opinion pairs. |
| **5.1.1 Basic Tech** | 3. NER Tagging | [extraction.py](file:///Users/aswinmenon/Downloads/8420-A2/GroupID_Assignment3/Codes/src/extraction.py) | `extract_named_entities()`: Extract brands, specs, locations. |
| **5.1.1 Basic Tech** | 4. Rule-Based IE | [extraction.py](file:///Users/aswinmenon/Downloads/8420-A2/GroupID_Assignment3/Codes/src/extraction.py) | `extract_prices_and_versions()`: Regex specs & prices matching. |
| **5.1.1 Basic Tech** | 5. Traditional ML Sentiment | [traditional_ml.py](file:///Users/aswinmenon/Downloads/8420-A2/GroupID_Assignment3/Codes/src/traditional_ml.py) | `TraditionalMLClassifier`: Out-of-the-box TF-IDF + Logistic Regression. |
| **5.1.1 Basic Tech** | 6. Text Similarity | [semantic_search.py](file:///Users/aswinmenon/Downloads/8420-A2/GroupID_Assignment3/Codes/src/semantic_search.py) | `SemanticSearchEngine`: Embeddings + Cosine similarity search. |
| **5.1.2 Advanced Tech** | 1. Foundation Models | [ollama_client.py](file:///Users/aswinmenon/Downloads/8420-A2/GroupID_Assignment3/Codes/src/ollama_client.py) | `OllamaOrchestrator`: In-depth connection and fallback logic. |
| **5.1.2 Advanced Tech** | 2. RAG System | [RAG_engine.py](file:///Users/aswinmenon/Downloads/8420-A2/GroupID_Assignment3/Codes/src/RAG_engine.py) | `retrieve_context_for_rag()`: SQLite metadata & reviews retrieval. |
| **5.1.2 Advanced Tech** | 3. Chain-of-Thought | [generator.py](file:///Users/aswinmenon/Downloads/8420-A2/GroupID_Assignment3/Codes/src/generator.py) | `generate_description()`: System instruction prompt directing multi-step CoT. |
| **5.1.2 Advanced Tech** | 4. Few-Shot Adaptation | [fraud_detection.py](file:///Users/aswinmenon/Downloads/8420-A2/GroupID_Assignment3/Codes/src/fraud_detection.py) | `classify_ai_review_llm()`: Labeled custom reviews injected in prompt context. |
| **5.1.2 Advanced Tech** | 5. Agentic Ensemble | [agent_ensemble.py](file:///Users/aswinmenon/Downloads/8420-A2/GroupID_Assignment3/Codes/src/agent_ensemble.py) | `IntellishopEnsembleCoordinator`: Fuses rule indicators, traditional ML, and LLMs. |
| **5.1.2 Advanced Tech** | 6. LLM-as-a-Judge | [evaluator.py](file:///Users/aswinmenon/Downloads/8420-A2/GroupID_Assignment3/Codes/src/evaluator.py) | `LLMasJudgeEvaluator`: independent Llama critique of Gemma's generation. |

---

## 🎨 Interactive Storefront Features

1. **Prompt-Based Semantic Search**: Natural-language search matching user intent (e.g. *"morning coffee helper"*) utilizing semantic sentence embeddings and cosine similarity against product descriptions.
2. **Multi-Dimensional Authenticity Engine**: Calculates a unified **Fraud Index Score (0%-100%)** combining:
   * *Stylometrics*: Lexical diversity (TTR) and capitalization.
   * *Rating Contradiction*: Compares Numerical stars vs. Traditional ML Sentiment Probability.
   * *Temporal Burstiness*: Flags users submitting rapid sequential reviews in SQLite histories.
   * *Few-Shot AI Detector*: Deploys Llama to audit and tag reviews likely written by AI agents.
3. **Aspect Sentiment Panel**: Showcases dynamic, granular reviews features, aspect nouns, and adjective opinion modifiers extracted via spaCy.
4. **Copywriting & Judge**: Click a button to invoke Gemma to synthesize a RAG-grounded product description, accompanied by a dynamic Llama-as-a-Judge scorecard displaying rating parameters and specific factual audits.
