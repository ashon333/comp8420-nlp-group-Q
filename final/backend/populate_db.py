import pandas as pd
import random
import os
import json
import uuid
import math
from datetime import datetime
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

try:
    from groq import Groq
except ImportError:
    Groq = None

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = "congo_shop"

def populate():
    print("Connecting to MongoDB...")
    client = MongoClient(MONGO_URL)
    db = client[DATABASE_NAME]
    
    # Drop existing collections for a fresh start
    db.products.drop()
    db.reviews.drop()
    db.categories.drop()
    
    print("Loading datasets...")
    data_dir = '../../dataset/'
    df1 = pd.read_csv(data_dir + 'Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv')
    df2 = pd.read_csv(data_dir + 'Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv')
    df3 = pd.read_csv(data_dir + '1429_1.csv', low_memory=False)
    df_all = pd.concat([df1, df2, df3], ignore_index=True)
    
    if 'name' in df_all.columns:
        df_all['name'] = df_all['name'].astype(str).str.split(',,,').str[0].str.strip()
        df_all = df_all[df_all['name'] != 'nan']
        
        # Select top 30 most reviewed products
        top_products = df_all['name'].value_counts().head(30).index.tolist()
        
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        llm_client = Groq(api_key=GROQ_API_KEY) if Groq else None
        
        products_to_insert = []
        reviews_to_insert = []
        print(f"Processing {len(top_products)} products...")
        
        for i, p in enumerate(top_products):
            cat = df_all[df_all['name'] == p]['categories'].iloc[0] if 'categories' in df_all.columns else 'Electronics'
            category = str(cat).split(',')[0]
            
            # Extract image URLs
            images = [f"https://picsum.photos/seed/{i+100}/300/300"]
            if 'imageURLs' in df_all.columns:
                urls = df_all[df_all['name'] == p]['imageURLs'].dropna()
                if len(urls) > 0:
                    url_str = str(urls.iloc[0])
                    extracted = [u.strip() for u in url_str.split(',') if u.strip()]
                    if extracted:
                        images = extracted[:5]
            
            # Generate description using LLM
            description = "A great product."
            if llm_client:
                reviews = df_all[df_all['name'] == p]['reviews.text'].dropna().head(5).tolist()
                if reviews:
                    rev_text = "\n".join([f"- {r[:100]}" for r in reviews])
                    prompt = f"Product: {p}\nCategory: {category}\nCustomer reviews:\n{rev_text}\nWrite a short, engaging 2-sentence marketing description for this product based on these reviews."
                    try:
                        res = llm_client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=100
                        )
                        description = res.choices[0].message.content.strip().strip('"').strip("'")
                    except Exception as e:
                        print("LLM Error for", p, ":", e)
            
            # Generate embedding for search
            text_for_embedding = f"Product: {p}. Category: {category}. Description: {description}"
            embedding = embedder.encode([text_for_embedding])[0].tolist()
            
            prod_doc = {
                "id": i,
                "name": p,
                "price": round(random.uniform(19.99, 299.99), 2),
                "category": category,
                "image": images[0],
                "images": images,
                "description": description,
                "embedding": embedding
            }
            products_to_insert.append(prod_doc)
            
            # Extract reviews for this product
            product_reviews_df = df_all[df_all['name'] == p].dropna(subset=['reviews.text'])
            for _, r in product_reviews_df.iterrows():
                try:
                    rating = float(r.get('reviews.rating', 0))
                    if math.isnan(rating):
                        rating = 0
                except:
                    rating = 0
                review_doc = {
                    "id": f"rev_{uuid.uuid4().hex[:8]}",
                    "product_id": i,
                    "user_nickname": str(r.get('reviews.username', 'anonymous')),
                    "rating": rating,
                    "text": str(r['reviews.text']),
                    "created_at": str(r.get('reviews.date', datetime.now().isoformat()))
                }
                reviews_to_insert.append(review_doc)
                
            print(f"Processed {i+1}/{len(top_products)}: {p[:30]}...")
            
        if products_to_insert:
            db.products.insert_many(products_to_insert)
            print("Successfully inserted products into MongoDB.")
            
        if reviews_to_insert:
            db.reviews.insert_many(reviews_to_insert)
            print(f"Successfully inserted {len(reviews_to_insert)} reviews into MongoDB.")
            
            # Create indexes
            db.reviews.create_index([("product_id", 1), ("rating", -1), ("created_at", -1)])
            db.products.create_index([("name", "text"), ("category", "text"), ("description", "text")])
            print("Created indexes.")
            
            print("\n--- Database Analysis ---")
            total_products = db.products.count_documents({})
            print(f"Total products in database: {total_products}")
            
            categories = db.products.distinct("category")
            print(f"Number of categories: {len(categories)}")
            print("Categories:")
            
            categories_to_insert = []
            for category in categories:
                count = db.products.count_documents({"category": category})
                print(f" - {category}: {count}")
                prod = db.products.find_one({"category": category}, {"image": 1})
                categories_to_insert.append({
                    "name": category,
                    "image": prod["image"] if prod and "image" in prod else "https://images.unsplash.com/photo-1550009158-9ebf69173e03?q=80&w=600"
                })
                
            if categories_to_insert:
                db.categories.insert_many(categories_to_insert)
                print(f"Successfully inserted {len(categories_to_insert)} categories into MongoDB.")
            print("-------------------------\n")
            
    client.close()
    print("Done!")

if __name__ == "__main__":
    populate()
