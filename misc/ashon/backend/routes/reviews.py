from fastapi import APIRouter, HTTPException
from typing import List
from models import Review, ReviewBase, ReviewAnalysis
import uuid
from datetime import datetime
import random

router = APIRouter()

# Mock reviews database
MOCK_REVIEWS = {
    "prod_1": [
        {
            "id": "rev_1", "product_id": "prod_1", "user_nickname": "CoffeeLover99", 
            "rating": 5, "text": "Absolutely love these beans! The aroma is fantastic and makes my mornings perfect.",
            "created_at": datetime.now(),
            "analysis": {
                "sentiment": "Positive", "is_positive": True, "does_recommend": True, 
                "written_using_ai": False, "is_fake_review": False, "matches_product": True
            }
        },
        {
            "id": "rev_2", "product_id": "prod_1", "user_nickname": "BotUserX", 
            "rating": 1, "text": "This product is the best thing ever created in the history of the universe. Buy it now. Very good product.",
            "created_at": datetime.now(),
            "analysis": {
                "sentiment": "Positive", "is_positive": True, "does_recommend": True, 
                "written_using_ai": True, "is_fake_review": True, "matches_product": False
            }
        }
    ]
}

def analyze_review_text(text: str) -> ReviewAnalysis:
    # Mock AI analysis based on keywords in the review text
    lower_text = text.lower()
    is_positive = "good" in lower_text or "great" in lower_text or "love" in lower_text or "perfect" in lower_text
    is_negative = "bad" in lower_text or "terrible" in lower_text or "hate" in lower_text
    
    sentiment = "Positive" if is_positive else ("Negative" if is_negative else "Neutral")
    does_recommend = is_positive
    
    # Fake/AI detection mock logic
    written_using_ai = "best thing ever created" in lower_text or len(text.split()) < 5 and not is_negative
    is_fake_review = written_using_ai or (rating == 5 and len(text) < 10)
    
    return ReviewAnalysis(
        sentiment=sentiment,
        is_positive=is_positive,
        does_recommend=does_recommend,
        written_using_ai=written_using_ai,
        is_fake_review=is_fake_review,
        matches_product=True # Usually true unless we detect spam
    )

@router.get("/products/{product_id}/reviews", response_model=List[Review])
async def get_reviews(product_id: str):
    return MOCK_REVIEWS.get(product_id, [])

@router.post("/products/{product_id}/reviews", response_model=Review)
async def create_review(product_id: str, review: ReviewBase):
    # Perform Analysis
    analysis = analyze_review_text(review.text)
    
    # If the user specifically said something unrelated, maybe tweak matches_product (mock logic)
    if "car" in review.text.lower() and "coffee" not in review.text.lower():
        analysis.matches_product = False

    new_review = Review(
        id=f"rev_{uuid.uuid4().hex[:8]}",
        product_id=product_id,
        user_nickname=review.user_nickname,
        rating=review.rating,
        text=review.text,
        created_at=datetime.now(),
        analysis=analysis
    )
    
    if product_id not in MOCK_REVIEWS:
        MOCK_REVIEWS[product_id] = []
        
    MOCK_REVIEWS[product_id].append(new_review.dict())
    
    return new_review
