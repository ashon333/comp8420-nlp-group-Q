from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ReviewBase(BaseModel):
    user_nickname: str
    rating: int = Field(..., ge=1, le=5)
    text: str

class ReviewAnalysis(BaseModel):
    sentiment: str # Positive, Negative, Neutral
    is_positive: bool
    does_recommend: bool
    written_using_ai: bool
    is_fake_review: bool
    matches_product: Optional[bool] = None

class Review(ReviewBase):
    id: str
    product_id: str
    created_at: datetime
    analysis: Optional[ReviewAnalysis] = None

class ProductBase(BaseModel):
    name: str
    description: str
    category: str
    price: float
    image_url: Optional[str] = None
    average_rating: float = 0.0

class Product(ProductBase):
    id: str

# Request models
class PromptSearchRequest(BaseModel):
    prompt: str

class NormalSearchRequest(BaseModel):
    query: str

class ImageSearchRequest(BaseModel):
    image_data_base64: str # In reality, we might use multipart/form-data for file uploads
