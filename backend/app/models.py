# backend/app/models.py
from pydantic import BaseModel
from typing import List, Optional

class PerfumeBase(BaseModel):
    name: str
    brand: str
    notes: str
    price: Optional[float] = None
    rating: Optional[float] = None

class PerfumeResponse(PerfumeBase):
    id: int
    similarity_score: Optional[float] = None

class RecommendationRequest(BaseModel):
    perfume_name: str
    limit: int = 5
    min_similarity: float = 0.1

class RecommendationResponse(BaseModel):
    query_perfume: PerfumeResponse
    recommendations: List[PerfumeResponse]
    total_found: int