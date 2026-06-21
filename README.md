# Congo Shop: An E-commerce Intelligent System for Amazon Product Reviews

COMP8420 Advanced Natural Language Processing, Main Project (Assignment 3)
Use Case 6: E-commerce Intelligent System. Group Q.

## Overview

An end-to-end NLP/LLM system over the Datafiniti Amazon Product Reviews dataset.
It combines four basic NLP techniques (preprocessing, NER/POS, rule-based aspect
extraction, TF-IDF recommendation) with seven advanced LLM techniques (Llama 3.1
foundation model via Groq, RAG, prompt engineering, chain-of-thought, instruction
based aspect sentiment, an agentic ReAct pipeline, and LLM-as-a-judge). Results are
surfaced through the Congo Shop web application.

## Folder structure

```
Codes/
  Group_Q_final_notebook.ipynb   Main implementation (all NLP/LLM pipelines,
                                  evaluation, agent, and the FastAPI backend)
  frontend/                       Congo Shop web client (HTML, CSS, JavaScript, Tailwind via CDN)
    index.html                    Storefront: search + best-selling catalogue
    product-details.html          Product page, real-time sentiment, per-review AI analysis
    about.html, login.html        Static pages and login
    css/styles.css                Custom styles
    js/config.js                  API base URL (http://localhost:8000/api)
    js/auth.js, js/navbar.js      Client logic
  results/                        Generated figures and evaluation plots (.png)
  dataset/sample_reviews.csv      Small dataset sample for verification (add this, < 5 MB)
```

## Requirements

- Python 3.10+
- Jupyter, pandas, numpy, scikit-learn, nltk, spacy (en_core_web_sm),
  sentence-transformers, chromadb, groq, fastapi, uvicorn, pymongo
- MongoDB running locally (default: mongodb://localhost:27017)
- A Groq API key set in the environment (GROQ_API_KEY) for the LLM calls

Install (example):

```
pip install pandas numpy scikit-learn nltk spacy sentence-transformers \
            chromadb groq fastapi uvicorn pymongo
python -m spacy download en_core_web_sm
```

## How to run

1. Place the three Datafiniti CSV files in the dataset path referenced at the top
   of the notebook (or update the path).
2. Open `Group_Q_final_notebook.ipynb` and run the cells top to bottom. This runs
   the full pipeline: preprocessing, NER/POS, rule-based extraction, TF-IDF
   recommendation, LLM summarisation/description/insight, RAG, prompt-strategy
   comparison, aspect sentiment, the ReAct agent, and all evaluations. Figures are
   written to `results/`.
3. The backend (FastAPI + MongoDB) is defined in the notebook. Running those cells
   populates MongoDB and serves the REST API on `http://localhost:8000` with
   endpoints for products, reviews and per-review AI analysis.
4. With the backend running, open `frontend/index.html` (or serve the `frontend/`
   folder with any static server) to use the Congo Shop UI. `js/config.js` points
   the client at the local API.

## Notes

- All code is the group's own work. No LLM platform was used to generate project code.
- Some LLM calls depend on Groq availability; rate limits may affect exact reruns.
- A demonstration video is included in the submission under `Video/`.

```

```
