from fastapi import APIRouter, Request, HTTPException
from typing import List
from models import Product, NormalSearchRequest, PromptSearchRequest
import uuid

router = APIRouter()

# Refreshed product database with premium sneakers/lifestyle products
MOCK_PRODUCTS = [
    {
        "id": "prod_1", "name": "AeroStride Velocity X", "description": "High-performance running shoe with carbon fiber plating and reactive nitrogen-infused foam.", 
        "category": "Running", "price": 189.99, "average_rating": 4.8, 
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80"
    },
    {
        "id": "prod_2", "name": "TerraGrip Trailblazer", "description": "Rugged off-road trail running shoe featuring ultra-durable Vibram outsoles and water-resistant materials.", 
        "category": "Trail", "price": 149.99, "average_rating": 4.5, 
        "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=600&q=80"
    },
    {
        "id": "prod_3", "name": "NimbusFloat Comfort Foam", "description": "Daily walking sneaker designed for supreme plushness and active orthopedic arch support.", 
        "category": "Comfort", "price": 129.99, "average_rating": 4.9, 
        "image_url": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=600&q=80"
    },
    {
        "id": "prod_4", "name": "ApexRunner Premium Knits", "description": "Ultra-lightweight breathable knit athletic sneakers designed for agility and speed drills.", 
        "category": "Running", "price": 165.00, "average_rating": 4.2, 
        "image_url": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600&q=80"
    },
    {
        "id": "prod_5", "name": "RetroVolt Classic Leather", "description": "Timeless retro lifestyle sneaker styled with genuine vintage leather and vibrant color accents.", 
        "category": "Lifestyle", "price": 110.00, "average_rating": 4.7, 
        "image_url": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=600&q=80"
    }
]

@router.get("/", response_model=List[Product])
async def get_top_products(request: Request):
    sorted_products = sorted(MOCK_PRODUCTS, key=lambda x: x["average_rating"], reverse=True)
    return sorted_products

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
    for prod in MOCK_PRODUCTS:
        if prod["id"] == product_id:
            return prod
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/search", response_model=List[Product])
async def normal_search(search_req: NormalSearchRequest):
    query = search_req.query.lower()
    results = [p for p in MOCK_PRODUCTS if query in p["name"].lower() or query in p["description"].lower() or query in p["category"].lower()]
    return results

@router.post("/semantic-search", response_model=List[Product])
async def semantic_search(search_req: PromptSearchRequest):
    prompt = search_req.prompt.lower()
    results = []
    
    # Advanced sneaker-specific intent matching
    if "trail" in prompt or "hike" in prompt or "mountain" in prompt or "rough" in prompt:
        results = [p for p in MOCK_PRODUCTS if p["category"] == "Trail"]
    elif "run" in prompt or "fast" in prompt or "sport" in prompt or "speed" in prompt:
        results = [p for p in MOCK_PRODUCTS if p["category"] == "Running"]
    elif "comfortable" in prompt or "walk" in prompt or "ortho" in prompt or "soft" in prompt:
        results = [p for p in MOCK_PRODUCTS if p["category"] == "Comfort"]
    elif "casual" in prompt or "daily" in prompt or "retro" in prompt or "style" in prompt:
        results = [p for p in MOCK_PRODUCTS if p["category"] == "Lifestyle"]
    else:
        results = MOCK_PRODUCTS[:3]
        
    return results
