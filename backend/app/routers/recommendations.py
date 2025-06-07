# backend/app/routers/recommendations.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..models import RecommendationRequest, RecommendationResponse, PerfumeResponse
from ..recommender import PerfumeRecommender

router = APIRouter()
recommender = PerfumeRecommender()

@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get perfume recommendations based on similarity"""
    result = recommender.get_recommendations(
        request.perfume_name, 
        request.limit, 
        request.min_similarity
    )
    
    if result is None:
        raise HTTPException(status_code=404, detail="Perfume not found")
    
    return result

@router.get("/recommend/{perfume_name}")
async def get_recommendations_simple(
    perfume_name: str,
    limit: int = Query(5, ge=1, le=20),
    min_similarity: float = Query(0.1, ge=0.0, le=1.0)
):
    """Simple GET endpoint for recommendations"""
    result = recommender.get_recommendations(perfume_name, limit, min_similarity)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Perfume not found")
    
    return result

@router.get("/search")
async def search_perfumes(
    query: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50)
):
    """Search for perfumes by name or brand"""
    from ..database import get_db_connection
    import pandas as pd
    
    conn = get_db_connection()
    sql_query = """
    SELECT Name, Brand, Notes FROM perfumes 
    WHERE LOWER(Name) LIKE LOWER(?) OR LOWER(Brand) LIKE LOWER(?)
    LIMIT ?
    """
    df = pd.read_sql_query(sql_query, conn, params=[f"%{query}%", f"%{query}%", limit])
    conn.close()
    
    return df.to_dict('records')