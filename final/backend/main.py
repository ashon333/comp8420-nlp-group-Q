from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import re
from pymongo import MongoClient
import numpy as np
import uuid
from datetime import datetime

try:
    from groq import Groq
except ImportError:
    Groq = None

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

app = FastAPI(title="Congo Shop API")

_local_text_pipeline = None
_local_vision_pipeline = None


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = "congo_shop"

client = None
db = None
embedder = None

def init_app():
    global client, db, embedder
    try:
        client = MongoClient(MONGO_URL)
        db = client[DATABASE_NAME]
        print("Connected to MongoDB.")
    except Exception as e:
        print("MongoDB Connection Error:", e)
    
    if SentenceTransformer:
        embedder = SentenceTransformer('all-MiniLM-L6-v2')

@app.on_event("startup")
def on_startup():
    init_app()

@app.on_event("shutdown")
def on_shutdown():
    if client:
        client.close()

def doc_to_dict(doc):
    doc["_id"] = str(doc["_id"])
    if "embedding" in doc:
        del doc["embedding"] # don't send embedding to frontend
    return doc

@app.get("/api/products")
def get_products():
    if db is None:
        return {"products": []}
    prods = list(db.products.find({}, {"embedding": 0}).limit(20))
    return {"products": [doc_to_dict(p) for p in prods]}

@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    if db is None:
        raise HTTPException(status_code=500, detail="DB not connected")
    prod = db.products.find_one({"id": product_id}, {"embedding": 0})
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return doc_to_dict(prod)

@app.get("/api/categories")
def get_categories():
    if db is None:
        return {"categories": []}
        
    cats = list(db.categories.find({}, {"_id": 0}))
    return {"categories": cats}

class ReviewRequest(BaseModel):
    user_nickname: str
    rating: int
    text: str

@app.get("/api/products/{product_id}/reviews")
def get_reviews(product_id: int, rating: int = None, sort_by: str = "newest", page: int = 1, limit: int = 10):
    if db is None:
        return {"reviews": [], "total": 0, "page": page, "pages": 0}
        
    query = {"product_id": product_id}
    if rating is not None and rating > 0:
        query["rating"] = rating
        
    total = db.reviews.count_documents(query)
    skip = (page - 1) * limit
    
    cursor = db.reviews.find(query)
    
    if sort_by == "newest":
        cursor = cursor.sort("created_at", -1)
    elif sort_by == "oldest":
        cursor = cursor.sort("created_at", 1)
    elif sort_by == "highest":
        cursor = cursor.sort("rating", -1)
    elif sort_by == "lowest":
        cursor = cursor.sort("rating", 1)
        
    cursor = cursor.skip(skip).limit(limit)
    reviews = list(cursor)
    pages = (total + limit - 1) // limit if limit > 0 else 0
    return {
        "reviews": [doc_to_dict(r) for r in reviews],
        "total": total,
        "page": page,
        "pages": pages
    }

@app.post("/api/products/{product_id}/reviews")
def create_review(product_id: int, review: ReviewRequest):
    if db is None:
        raise HTTPException(status_code=500, detail="DB not connected")
    
    # Simple mock analysis
    lower_text = review.text.lower()
    is_positive = "good" in lower_text or "great" in lower_text or "love" in lower_text
    is_negative = "bad" in lower_text or "terrible" in lower_text or "hate" in lower_text
    
    analysis = {
        "sentiment": "Positive" if is_positive else ("Negative" if is_negative else "Neutral"),
        "does_recommend": not is_negative,
        "written_using_ai": "best thing ever" in lower_text,
        "is_fake_review": False,
        "matches_product": True
    }
    
    new_review = {
        "id": f"rev_{uuid.uuid4().hex[:8]}",
        "product_id": product_id,
        "user_nickname": review.user_nickname,
        "rating": review.rating,
        "text": review.text,
        "created_at": datetime.now().isoformat(),
        "analysis": analysis
    }
    
    db.reviews.insert_one(new_review.copy())
    return doc_to_dict(new_review)

@app.get("/api/reviews/{review_id}/analysis")
def analyze_single_review(review_id: str):
    if db is None:
        raise HTTPException(status_code=500, detail="DB not connected")
        
    review = db.reviews.find_one({"id": review_id})
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
        
    if "analysis" in review:
        return review["analysis"]
        
    # Use LLM to analyze the review
    llm_client = Groq(api_key=GROQ_API_KEY) if Groq else None
    
    lower_text = review.get("text", "").lower()
    is_positive = "good" in lower_text or "great" in lower_text or "love" in lower_text
    is_negative = "bad" in lower_text or "terrible" in lower_text or "hate" in lower_text
    
    analysis = {
        "sentiment": "Positive" if is_positive else ("Negative" if is_negative else "Neutral"),
        "does_recommend": not is_negative,
        "written_using_ai": "best thing ever" in lower_text,
        "is_fake_review": False,
        "matches_product": True
    }
    
    if llm_client:
        prompt = f"""Review: "{review.get('text', '')[:500]}"
Analyze this review and provide a JSON response with the following keys exactly:
- "sentiment" (string: "Positive", "Negative", or "Neutral")
- "does_recommend" (boolean)
- "written_using_ai" (boolean)
- "is_fake_review" (boolean)
- "matches_product" (boolean)
Return ONLY valid JSON:"""
        try:
            res = llm_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.1
            )
            content = res.choices[0].message.content
                
            import re, json
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                parsed = json.loads(match.group())
                # ensure all keys exist
                for k in analysis.keys():
                    if k in parsed:
                        analysis[k] = parsed[k]
        except Exception as e:
            print("LLM Error:", e)

    # Save to db
    db.reviews.update_one({"id": review_id}, {"$set": {"analysis": analysis}})
    
    return analysis

@app.get("/api/products/{product_id}/analysis")
def get_product_analysis(product_id: int):
    if db is None:
        raise HTTPException(status_code=500, detail="DB not connected")
        
    reviews = list(db.reviews.find({"product_id": product_id}))
    if not reviews:
        return {
            "avg_rating": 0,
            "pct_positive": 0,
            "pct_negative": 0,
            "aspect_scores": {}
        }
        
    ratings = [r.get("rating", 0) for r in reviews if r.get("rating")]
    avg_r = sum(ratings) / len(ratings) if ratings else 0
    pct_pos = sum(1 for r in ratings if r >= 4) / len(ratings) * 100 if ratings else 0
    pct_neg = sum(1 for r in ratings if r <= 2) / len(ratings) * 100 if ratings else 0
    
    # Sample up to 5 reviews for LLM
    reviews_to_sample = 20
    import random
    sample_reviews = [r for r in reviews if len(r.get("text", "").split()) >= 10]
    if len(sample_reviews) > reviews_to_sample:
        sample_reviews = random.sample(sample_reviews, reviews_to_sample)
    elif len(sample_reviews) == 0:
        sample_reviews = reviews[:reviews_to_sample]
        
    aspects = ['quality', 'price', 'usability', 'performance']
    asp_totals = {a: [] for a in aspects}
    s_map = {'Positive': 1, 'Neutral': 0, 'Negative': -1, 'Not_Mentioned': None}
    
    llm_client = Groq(api_key=GROQ_API_KEY) if Groq else None
    
    if sample_reviews:
        for row in sample_reviews:
            text = str(row.get("text", ""))[:300]
            parsed = None
            if llm_client:
                prompt = (f'Review: "{text}"\n'
                          f'For each aspect give: Positive/Negative/Neutral/Not_Mentioned.\n'
                          f'JSON only: {{"quality":"...","price":"...","usability":"...","performance":"..."}}')
                try:
                    res = llm_client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "You are a sentiment analyst. Respond only with JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.1
                    )
                    resp = res.choices[0].message.content
                    jm = re.search(r'\{.*\}', resp or '', re.DOTALL)
                    if jm:
                        parsed = json.loads(jm.group())
                except Exception as e:
                    print("LLM error in analysis:", e)
            
            if not parsed:
                # Local heuristic fallback
                lower_text = text.lower()
                is_pos = "good" in lower_text or "great" in lower_text or "excellent" in lower_text or "love" in lower_text
                is_neg = "bad" in lower_text or "terrible" in lower_text or "poor" in lower_text or "hate" in lower_text
                
                base_sentiment = "Positive" if is_pos else ("Negative" if is_neg else "Neutral")
                parsed = {
                    "quality": base_sentiment,
                    "price": base_sentiment,
                    "usability": base_sentiment,
                    "performance": base_sentiment
                }
                
            for asp in aspects:
                v = s_map.get(parsed.get(asp, 'Not_Mentioned'), None)
                if v is not None:
                    asp_totals[asp].append(v)
                
    aspect_scores = {a: round(float(np.mean(v)), 3) if v else 0.0 for a, v in asp_totals.items()}
    
    return {
        "avg_rating": round(avg_r, 2),
        "pct_positive": round(pct_pos, 1),
        "pct_negative": round(pct_neg, 1),
        "aspect_scores": aspect_scores
    }

class SearchRequest(BaseModel):
    query: str

class ImageSearchRequest(BaseModel):
    image_data_url: str

@app.post("/api/images/search")
def search_products_by_image(req: ImageSearchRequest):
    if db is None or not embedder:
        return {"results": []}
    
    llm_client = Groq(api_key=GROQ_API_KEY) if Groq else None
    if not llm_client:
        return {"results": []}
        
    try:
        res = llm_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe the core product or object in this image in a concise search query (1-4 words). Only output the item name."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": req.image_data_url,
                            },
                        },
                    ],
                }
            ],
            temperature=0.1,
            max_tokens=20
        )
        query = res.choices[0].message.content.strip()
    except Exception as e:
        print("Vision LLM error:", e)
        return {"results": []}
        
    q_emb = embedder.encode([query])[0]
    
    all_prods = list(db.products.find({}))
    if not all_prods:
        return {"results": []}
        
    scored = []
    for p in all_prods:
        if "embedding" not in p:
            continue
        p_emb = np.array(p["embedding"])
        sim = np.dot(q_emb, p_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(p_emb))
        scored.append((sim, p))
        
    scored.sort(key=lambda x: x[0], reverse=True)
    top_5 = [doc_to_dict(s[1]) for s in scored[:5]]
    
    return {"results": top_5, "query_used": query}

@app.post("/api/search")
def search_products(req: SearchRequest):
    if db is None:
        return {"results": []}
    
    if not embedder:
        # Fallback to MongoDB text search if no embedder
        res = db.products.find({"$text": {"$search": req.query}}, {"embedding": 0}).limit(5)
        return {"results": [doc_to_dict(p) for p in res]}
    
    # Semantic Search using in-memory cosine similarity over MongoDB documents
    q_emb = embedder.encode([req.query])[0]
    
    all_prods = list(db.products.find({}))
    if not all_prods:
        return {"results": []}
        
    scores = []
    for p in all_prods:
        if "embedding" in p and p["embedding"]:
            p_emb = np.array(p["embedding"])
            score = np.dot(q_emb, p_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(p_emb) + 1e-10)
            scores.append((score, p))
            
    scores.sort(key=lambda x: x[0], reverse=True)
    top_results = [doc_to_dict(p[1]) for p in scores[:5]]
    
    return {"results": top_results}

@app.post("/api/multimodal")
async def multimodal_search(file: UploadFile = File(None), prompt: str = Form(None)):
    query = ""
    if prompt:
        query += prompt + " "
    if file:
        query += file.filename.replace(".jpg", "").replace(".png", "").replace("-", " ")
    
    if not query.strip():
        query = "electronics"

    if db is None:
        return {"message": "DB Error", "results": []}

    if embedder:
        q_emb = embedder.encode([query])[0]
        all_prods = list(db.products.find({}))
        scores = []
        for p in all_prods:
            if "embedding" in p and p["embedding"]:
                p_emb = np.array(p["embedding"])
                score = np.dot(q_emb, p_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(p_emb) + 1e-10)
                scores.append((score, p))
        scores.sort(key=lambda x: x[0], reverse=True)
        top_results = [doc_to_dict(p[1]) for p in scores[:3]]
    else:
        top_results = [doc_to_dict(p) for p in db.products.find({}, {"embedding": 0}).limit(3)]
        
    return {
        "message": f"Analyzed multimodal input: {query.strip()}",
        "results": top_results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
