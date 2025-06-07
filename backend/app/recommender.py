# backend/app/recommender.py
import pandas as pd
import numpy as np
from .database import get_db_connection, load_similarity_data
from .models import PerfumeResponse

class PerfumeRecommender:
    def __init__(self):
        self.similarity_data = load_similarity_data()
        self.similarity_matrix = self.similarity_data['similarity_matrix']
    
    def get_perfume_by_name(self, name: str):
        """Find perfume by name (case insensitive)"""
        conn = get_db_connection()
        query = """
        SELECT * FROM perfumes 
        WHERE LOWER(Name) LIKE LOWER(?) 
        LIMIT 1
        """
        df = pd.read_sql_query(query, conn, params=[f"%{name}%"])
        conn.close()
        
        if df.empty:
            return None
        return df.iloc[0]
    
    def get_recommendations(self, perfume_name: str, limit: int = 5, min_similarity: float = 0.1):
        """Get perfume recommendations"""
        # Find the input perfume
        perfume = self.get_perfume_by_name(perfume_name)
        if perfume is None:
            return None
        
        # Get all perfumes for index mapping
        conn = get_db_connection()
        all_perfumes = pd.read_sql_query("SELECT * FROM perfumes", conn)
        conn.close()
        
        # Find the index of the input perfume
        perfume_idx = all_perfumes[all_perfumes['Name'].str.lower() == perfume['Name'].lower()].index[0]
        
        # Get similarity scores
        similarity_scores = self.similarity_matrix[perfume_idx].toarray().flatten()
        
        # Get top similar perfumes (excluding the input perfume itself)
        similar_indices = np.argsort(similarity_scores)[::-1]
        similar_indices = similar_indices[similar_indices != perfume_idx]
        
        recommendations = []
        for idx in similar_indices:
            score = similarity_scores[idx]
            if score < min_similarity:
                break
            if len(recommendations) >= limit:
                break
                
            rec_perfume = all_perfumes.iloc[idx]
            recommendations.append(PerfumeResponse(
                id=int(idx),
                name=rec_perfume['Name'],
                brand=rec_perfume['Brand'],
                notes=rec_perfume['Notes'],
                similarity_score=float(score)
            ))
        
        query_perfume = PerfumeResponse(
            id=perfume_idx,
            name=perfume['Name'],
            brand=perfume['Brand'],
            notes=perfume['Notes']
        )
        
        return {
            "query_perfume": query_perfume,
            "recommendations": recommendations,
            "total_found": len(recommendations)
        }